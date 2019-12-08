/*
 * IRremote
 * Version 0.11 August, 2009
 * Copyright 2009 Ken Shirriff
 * For details, see http://arcfn.com/2009/08/multi-protocol-infrared-remote-library.html
 *
 * Modified by Paul Stoffregen <paul@pjrc.com> to support other boards and timers
 * Modified  by Mitra Ardron <mitra@mitra.biz> 
 * Added Sanyo and Mitsubishi controllers
 * Modified Sony to spot the repeat codes that some Sony's send
 * 
 * Modifier by
 * Interrupt code based on NECIRrcv by Joe Knapp
 * http://www.arduino.cc/cgi-bin/yabb2/YaBB.pl?num=1210243556
 * Also influenced by http://zovirl.com/2008/11/12/building-a-universal-remote-with-an-arduino/
 *
 * JVC and Panasonic protocol added by Kristian Lauszus (Thanks to zenwheel and other people at the original blog post)
 */

#include "IRSendRev.h"
#include "IRSendRevInt.h"

// Provides ISR
#include <avr/interrupt.h>

volatile irparams_t irparams;

void IRSendRev::sendRaw(unsigned int buf[], int len, int hz)
{
  EnableIROut(hz);

  for (int i = 0; i < len; i++)
  {
    if (i & 1)
    {
      space(buf[i]);
    }
    else
    {
      mark(buf[i]);
    }
  }
  space(0); // Just to be sure
}

void IRSendRev::mark(int time)
{
  // Sends an IR mark for the specified number of microseconds.
  // The mark output is modulated at the PWM frequency.
  TIMER_ENABLE_PWM; // Enable pin 3 PWM output
  delayMicroseconds(time);
}

/* Leave pin off for time (given in microseconds) */
void IRSendRev::space(int time)
{
  // Sends an IR space for the specified number of microseconds.
  // A space is no output, so the PWM output is disabled.
  TIMER_DISABLE_PWM; // Disable pin 3 PWM output
  delayMicroseconds(time);
}

void IRSendRev::EnableIROut(int khz)
{
  // Enables IR output.  The khz value controls the modulation frequency in kilohertz.
  // The IR output will be on pin 3 (OC2B).
  // This routine is designed for 36-40KHz; if you use it for other values, it's up to you
  // to make sure it gives reasonable results.  (Watch out for overflow / underflow / rounding.)
  // TIMER2 is used in phase-correct PWM mode, with OCR2A controlling the frequency and OCR2B
  // controlling the duty cycle.
  // There is no prescaling, so the output frequency is 16MHz / (2 * OCR2A)
  // To turn the output on and off, we leave the PWM running, but connect and disconnect the output pin.
  // A few hours staring at the ATmega documentation and this will all make sense.
  // See my Secrets of Arduino PWM at http://arcfn.com/2009/07/secrets-of-arduino-pwm.html for details.

  // Disable the Timer2 Interrupt (which is used for receiving IR)
  TIMER_DISABLE_INTR; //Timer2 Overflow Interrupt

  pinMode(TIMER_PWM_PIN, OUTPUT);
  digitalWrite(TIMER_PWM_PIN, LOW); // When not sending PWM, we want it low

  TIMER_CONFIG_KHZ(khz);
  TIMER_ENABLE_PWM;
}

void IRSendRev::ClearNew()
{
  IRBufferCounter = 0;
  MessageCharCount = 0;
  start_h = 0;
  start_l = 0;
  first = 0;
  ready = false;
  irparams.rcvstate = STATE_IDLE;
  ClearSRBuffer();
}

void IRSendRev::ClearSRBuffer()
{
  for (int i = 0; i < MaxMsgSize; i++)
  {
    SendReceiveBuffer[i] = '\n';
  }
}

void IRSendRev::Init(int revPin)
{
  irparams.recvpin = revPin;
  IRBufferCounter = 0;
  MessageCharCount = 0;
  start_h = 0;
  start_l = 0;
  first = 0;
  ready = false;
  EnableIRIn(); // Start the receiver
  delay(20);
  ClearNew();
}

void IRSendRev::Init()
{
  IRBufferCounter = 0;
  MessageCharCount = 0;
  start_h = 0;
  start_l = 0;
  first = 0;
  ready = false;
  delay(20);
  ClearNew();
}
// initialization
void IRSendRev::EnableIRIn()
{
  cli();
  // setup pulse clock timer interrupt
  //Prescale /8 (16M/8 = 0.5 microseconds per tick)
  // Therefore, the timer interval can range from 0.5 to 128 microseconds
  // depending on the reset value (255 to 0)
  TIMER_CONFIG_NORMAL();

  //Timer2 Overflow Interrupt Enable
  TIMER_ENABLE_INTR;

  TIMER_RESET;

  sei(); // enable interrupts

  // initialize state machine variables
  irparams.rcvstate = STATE_IDLE;
  //irparams.rawlen = 0;

  // set pin modes
  pinMode(irparams.recvpin, INPUT);
}

void CombineIRBuffer()
{
  if (IR.first == 0)
    IR.first = IR.IRBuffer[0];
  else if (IR.start_h == 0)
    IR.start_h = IR.IRBuffer[0];
  else if (IR.start_l == 0)
    IR.start_l = IR.IRBuffer[0];
  else
  {
    //determine short_time
    int short_time = 0;
    int long_time = 0;
    int long_count = 0;
    for (int i = 0; i < 16; i += 2)
    {
      short_time += IR.IRBuffer[i];
    }
    short_time /= 8;
    for (int i = 1; i < 16; i += 2)
    {
      if (IR.IRBuffer[i] > (2 * short_time))
      {
        long_time += IR.IRBuffer[i];
        long_count++;
      }
    }
    IR.long_time = long_time;   // / long_count;
    IR.short_time = short_time; // / long_count;
    short_time *= 2;            //getting the doubled of the average short time
    IR.SendReceiveBuffer[IR.MessageCharCount] = 0x00;
    for (int i = 1; i < 8; i++)
    {
      if (IR.IRBuffer[1 + 2 * i] > (2 * short_time)) //1
      {
        IR.SendReceiveBuffer[IR.MessageCharCount] |= 0x01 << (7 - i);
      }
      else
      {
        IR.SendReceiveBuffer[IR.MessageCharCount] &= ~(0x01 << (7 - i));
      }
    }
    IR.MessageCharCount++;
  }
  IR.IRBufferCounter = 0;
}

void incstuff()
{
  Serial.println("ja");
  CombineIRBuffer();
}

// TIMER2 interrupt code to collect raw data.
// Widths of alternating SPACE, MARK are recorded in rawbuf.
// Recorded in ticks of 50 microseconds.
// rawlen counts the number of entries recorded so far.
// First entry is the SPACE between transmissions.
// As soon as a SPACE gets long, ready is set, state switches to IDLE, timing of SPACE continues.
// As soon as first MARK arrives, gap width is recorded, ready is cleared, and new logging starts

ISR(TIMER_INTR_NAME)
{
  TIMER_RESET;

  int irdata = (int)digitalRead(irparams.recvpin);

  irparams.timer++; // One more 50us tick
  if (IR.MessageCharCount >= MaxMsgSize)
  {
    // Buffer overflow
    IR.ValidateOrThrowInput();
    //irparams.rcvstate = STATE_STOP;
  }
  switch (irparams.rcvstate)
  {
  case STATE_IDLE: // In the middle of a gap
    if (irdata == MARK)
    {
      if (irparams.timer < GAP_TICKS)
      {
        // Not big enough to be a gap.
        irparams.timer = 0;
      }
      else
      {
        // gap just ended, record duration and start recording transmission
        //irparams.rawlen = 0;
        IR.IRBufferCounter = 0;
        IR.IRBuffer[IR.IRBufferCounter++] = irparams.timer;
        //irparams.rawbuf[irparams.rawlen++] = irparams.timer;
        if (IR.IRBufferCounter == 16 || IR.start_h == 0 || IR.start_l == 0 || IR.first == 0)
          CombineIRBuffer();

        irparams.timer = 0;
        irparams.rcvstate = STATE_MARK;
      }
    }
    break;
  case STATE_MARK: // timing MARK
    if (irdata == SPACE)
    { // MARK ended, record time
      IR.IRBuffer[IR.IRBufferCounter++] = irparams.timer;
      //irparams.rawbuf[irparams.rawlen++] = irparams.timer;
      if (IR.IRBufferCounter == 16 || IR.start_h == 0 || IR.start_l == 0 || IR.first == 0)
        CombineIRBuffer();

      irparams.timer = 0;
      irparams.rcvstate = STATE_SPACE;
    }
    break;
  case STATE_SPACE: // timing SPACE
    if (irdata == MARK)
    { // SPACE just ended, record it
      IR.IRBuffer[IR.IRBufferCounter++] = irparams.timer;
      //irparams.rawbuf[irparams.rawlen++] = irparams.timer;
      if (IR.IRBufferCounter == 16 || IR.start_h == 0 || IR.start_l == 0 || IR.first == 0)
        CombineIRBuffer();

      irparams.timer = 0;
      irparams.rcvstate = STATE_MARK;
    }
    else
    { // SPACE
      if (irparams.timer > GAP_TICKS)
      {
        // big SPACE, indicates gap between codes
        // Mark current code as ready for processing
        // Switch to STOP
        // Don't reset timer; keep counting space width
        IR.ValidateOrThrowInput();
        irparams.rcvstate = STATE_STOP;
      }
    }
    break;
  case STATE_STOP: // waiting, measuring gap
    if (irdata == MARK)
    { // reset gap timer
      irparams.timer = 0;
    }
    break;
  }
}

/*void IRSendRev::Clear()
{
  irparams.rcvstate = STATE_IDLE;
  //irparams.rawlen = 0;
}*/

// Decodes the received IR message
// Returns 0 if no data ready, 1 if data ready.
// Results of decoding are stored in results
int IRSendRev::decode(decode_results *results)
{
  //results->rawbuf = irparams.rawbuf;
  //results->rawlen = irparams.rawlen;
  if (irparams.rcvstate != STATE_STOP)
  {
    return ERR;
  }
  // Throw away and start over
  ClearNew();
  return 1;
}

unsigned char IRSendRev::Recv(unsigned char *revData)
{ /*
  int count = results.rawlen;
  int nshort = 0;
  int nlong = 0;
  int count_data = 0;

  count_data = (count - 4) / 16;

  for (int i = 0; i < 10; i++) // count nshort
  {
    nshort += results.rawbuf[3 + 2 * i];
  }
  nshort /= 10;

  int i = 0;
  int j = 0;
  while (1) // count nlong
  {
    if (results.rawbuf[4 + 2 * i] > (2 * nshort))
    {
      nlong += results.rawbuf[4 + 2 * i];
      j++;
    }
    i++;
    if (j == 10)
      break;
    if ((4 + 2 * i) > (count - 10))
      break;
  }
  nlong /= j;

  int doubleshort = 2 * nshort;
  for (i = 0; i < count_data; i++)
  {
    revData[i + D_DATA] = 0x00;
    for (j = 0; j < 8; j++)
    {
      if (results.rawbuf[4 + 16 * i + j * 2] > doubleshort) // 1
      {
        revData[i + D_DATA] |= 0x01 << (7 - j);
      }
      else
      {
        revData[i + D_DATA] &= ~(0x01 << (7 - j));
      }
    }
  }
  revData[D_LEN] = count_data + 5;
  revData[D_STARTH] = results.rawbuf[1];
  revData[D_STARTL] = results.rawbuf[2];
  revData[D_SHORT] = nshort;
  revData[D_LONG] = nlong;
  revData[D_DATALEN] = count_data;

#if __DEBUG
  Serial.print("\r\n*************************************************************\r\n");
  Serial.print("len\t = ");
  Serial.println(revData[D_LEN]);
  Serial.print("start_h\t = ");
  Serial.println(revData[D_STARTH]);
  Serial.print("start_l\t = ");
  Serial.println(revData[D_STARTL]);
  Serial.print("short\t = ");
  Serial.println(revData[D_SHORT]);
  Serial.print("long\t = ");
  Serial.println(revData[D_LONG]);
  Serial.print("data_len = ");
  Serial.println(revData[D_DATALEN]);
  for (int i = 0; i < revData[D_DATALEN]; i++)
  {
    Serial.print(revData[D_DATA + i]);
    Serial.print("\t");
  }
  Serial.print("\r\n*************************************************************\r\n");
#endif

  Clear(); // Receive the next value
  return revData[D_LEN] + 1;
*/
  return 0;
}

//if get some data from IR
unsigned char IRSendRev::IsDta()
{
  return ((MessageCharCount != 0) ? 1 : 0);
}

void IRSendRev::ImpSendRaw(unsigned int time, bool *toggleFlag)
{
  if (*toggleFlag)
  {
    space(time * 50);
  }
  else
  {
    mark(time * 50);
  }
  // toggle
  *toggleFlag = !(*toggleFlag);
}

// wrote my Own, cause their function succs regarding optimization
void IRSendRev::ImpSend(unsigned char *idata, unsigned char ifreq)
{
  int len = idata[D_LEN];
  unsigned int start_high = idata[D_STARTH];
  unsigned int start_low = idata[D_STARTL];
  unsigned int nshort = idata[D_SHORT];
  unsigned int nlong = idata[D_LONG];
  unsigned char datalen = idata[D_DATALEN]; //need to manually set this

  int realDatalen = (datalen == 0) ? MaxMsgSize : datalen;

#if __DEBUG
  Serial.println("begin to send ir:\r\n");
  Serial.print("ifreq = ");
  Serial.println(ifreq);
  Serial.print("len = ");
  Serial.println(len);
  Serial.print("start_high = ");
  Serial.println(start_high);
  Serial.print("start_low = ");
  Serial.println(start_low);
  Serial.print("nshort = ");
  Serial.println(nshort);
  Serial.print("nlong = ");
  Serial.println(nlong);
  Serial.print("datalen = ");
  Serial.println(realDatalen);
#endif

  bool toggle = false;
  bool *toggleFlag = &toggle;

  EnableIROut(ifreq);

  // send starting
  ImpSendRaw(start_high, toggleFlag);
  // equal = !equal;
  ImpSendRaw(start_low, toggleFlag);
  // send data:

  for (int i = /*D_DATA*/ 0; i < realDatalen; i++)
  {
    for (int j = 0; j < 8; j++)
    {
      if (idata[6 + i] & 0x01 << (7 - j))
      {
        ImpSendRaw(nshort, toggleFlag);
        ImpSendRaw(nlong, toggleFlag);
      }
      else
      {
        ImpSendRaw(nshort, toggleFlag);
        ImpSendRaw(nshort, toggleFlag);
      }
    }
  }

  //send ending
  ImpSendRaw(nshort, toggleFlag);
  ImpSendRaw(nshort, toggleFlag);

  space(0); //they said "Just to be sure" yeah, why not
}

void IRSendRev::ValidateOrThrowInput()
{
  // maybe filterig here could be possible but doing it in the main ard script is easier
  ready = true;
}

void IRSendRev::Send(unsigned char *idata, unsigned char ifreq)
{
  int len = idata[0];
  unsigned char start_high = idata[1];
  unsigned char start_low = idata[2];
  unsigned char nshort = idata[3];
  unsigned char nlong = idata[4];
  unsigned char datalen = idata[5];

  unsigned int *pSt = (unsigned int *)malloc((4 + datalen * 16) * sizeof(unsigned int));

  if (NULL == pSt)
  {
#if __DEBUG
    Serial.println("not enough place!!\r\n");
#endif
    exit(1);
  }

#if __DEBUG
  Serial.println("begin to send ir:\r\n");
  Serial.print("ifreq = ");
  Serial.println(ifreq);
  Serial.print("len = ");
  Serial.println(len);
  Serial.print("start_high = ");
  Serial.println(start_high);
  Serial.print("start_low = ");
  Serial.println(start_low);
  Serial.print("nshort = ");
  Serial.println(nshort);
  Serial.print("nlong = ");
  Serial.println(nlong);
  Serial.print("datalen = ");
  Serial.println(datalen);
#endif

  pSt[0] = start_high * 50;
  pSt[1] = start_low * 50;

  for (int i = 0; i < datalen; i++)
  {
    for (int j = 0; j < 8; j++)
    {
      if (idata[6 + i] & 0x01 << (7 - j))
      {
        pSt[16 * i + 2 * j + 2] = nshort * 50;
        pSt[16 * i + 2 * j + 3] = nlong * 50;
      }
      else
      {
        pSt[16 * i + 2 * j + 2] = nshort * 50;
        pSt[16 * i + 2 * j + 3] = nshort * 50;
      }
    }
  }

  pSt[2 + datalen * 16] = nshort * 50;
  pSt[2 + datalen * 16 + 1] = nshort * 50;

#if __DEBUG
  for (int i = 0; i < 4 + datalen * 16; i++)
  {
    Serial.print(pSt[i]);
    Serial.print("\t");
  }
  Serial.println();
#endif
  sendRaw(pSt, 4 + datalen * 16, ifreq);
  free(pSt);
}

IRSendRev IR;
