/*
 * @author Kai Fischer
 * @email kathunfischer@googlemail.com
 * @desc the arduino program, handles the handshake and the real chatting loop of reading and writing messages
 * 
 * @info  this file was inspired by the files "https://github.com/Seeed-Studio/IRSendRev/blob/master/examples/send/send.ino" 
 *        and "https://github.com/Seeed-Studio/IRSendRev/blob/master/examples/recv/recv.ino" 
 */

#include "IRSendRev.h"

//defines from example
#define BIT_LEN 0
#define BIT_START_H 1
#define BIT_START_L 2
#define BIT_DATA_H 3
#define BIT_DATA_L 4
#define BIT_HANDSHAKE 5
#define BIT_DATA 6
#define GuidLength 36

//variable from example : define the base frequenz
const int ir_freq = 38; // 38k

//own variables:
int Arraylength;
const int pinRecv = 2; 

unsigned char SendRecBuffer[MaxMsgSize];

bool ConToHost;
unsigned char HostGuid[GuidLength];
unsigned char GuestGuid[GuidLength];
int InitStep;

void GetHostGuid()
{
    char GotGuidMsg[] = "~okay~\n";

    // save the Guid from Host
    for (int i = 0; i < GuidLength; i++)
    {
        HostGuid[i] = SendRecBuffer[i];
    }

    // confirm: got guid
    Serial.write(GotGuidMsg);
    ConToHost = true;
    InitStep = 2;
}

// clearing the SendRecieve Buffer
void ClearSendRecBuffer()
{
  Arraylength = 0; 
  SendRecBuffer[0] = '\n';
  for (int i = 1; i < MaxMsgSize; i++)
  {
    SendRecBuffer[i] = '\n';
  }
}

void CheckForHostInit()
{
    char PingInput[] = "~echo~\n";
    char PingOutput[] = "~ping~\n";

    // wait for correct Ping input request
    for (int i = 0; i < 5; i++)
    {
        if (SendRecBuffer[i] != PingInput[i])
        {
          ConToHost = false;
          return;
        }
    }

    // answer with correct ping output
    Serial.write(PingOutput);
    // getting ready for next step
    InitStep = 1;
}

void FlagsInit()
{
  SendRecBuffer[BIT_LEN] = 1;      // all data that needs to be sent
  SendRecBuffer[BIT_START_H] = 179; // the logic high duration of "Start"
  SendRecBuffer[BIT_START_L] = 90;  // the logic low duration of "Start"
  SendRecBuffer[BIT_DATA_H] = 10;   // the logic "long" duration in the communication
  SendRecBuffer[BIT_DATA_L] =95;   // the logic "short" duration in the communication
  SendRecBuffer[BIT_HANDSHAKE] = (Arraylength > 255)? 0 : Arraylength % 256;
}

// Send the Buffer to the host-computer using serial connection
void SerSend()
{
  if (SendRecBuffer[0] == '\n')
    return;
  for (int i = 0; i < MaxMsgSize; i++)
  {
    Serial.write(SendRecBuffer[i]);
    if (SendRecBuffer[i] == '\n')
      return;
  }
  // if the buffer did not contain a newline, add it
  if (SendRecBuffer[MaxMsgSize] != '\n')
    Serial.write('\n');
}

// Recieve Information from host-computer using serial and save it to the buffer
void SerRecieve()
{
  int i = (ConToHost)?BIT_DATA:0;
  while (Serial.available() && i < MaxMsgSize)
  {
    SendRecBuffer[i] = Serial.read();
    if (SendRecBuffer[i] == '\n')
      break;
    i++;
    if (Serial.available() == false)
      delay(2);
  }
  Arraylength = i;  
  if (ConToHost != false)FlagsInit();
}

void IRSend()
{
  if (SendRecBuffer[BIT_DATA] == '\n') return;
  IR.ImpSend(SendRecBuffer, 38);
  IR.ClearNew();
  IR.EnableIRIn();
}

void IRReceive()
{
  if(IR.ready)                  
  {
  if ((IR.start_l < 50 && IR.start_h > 0) || (IR.start_h < 50 && IR.start_h > 0) || IR.MessageCharCount == 0)
  {
    IR.ClearNew();
    return;
  }
  #if __DEBUG
      Serial.println("other:");
      Serial.print("start_l: ");Serial.print(IR.start_l);
      Serial.write('\n');
      Serial.print("start_h: ");Serial.print(IR.start_h);
      Serial.write('\n');
      Serial.print("data_len: ");Serial.print(IR.MessageCharCount);
      Serial.write('\n');        
      Serial.print("short_time: ");Serial.print(IR.short_time);
      Serial.write('\n');        
      Serial.print("long_time: ");Serial.print(IR.long_time);
      Serial.write('\n');
    #endif         
      for (int i=0; i<MaxMsgSize; i++)
      {
        SendRecBuffer[i] = IR.SendReceiveBuffer[i];
        if (IR.SendReceiveBuffer[i] == '\n') break;
      }
    IR.ClearNew();
  }
}

void setup()
{
  /*
  everytime the arduino connects to a host, it gets resetted
  and starts here, after the setup method the loop()-method will be executed as an endless loop 
  */
  Serial.begin(115200);
  ClearSendRecBuffer();

  ConToHost = false;
  InitStep = 0;
  for (int i = 0; i < GuidLength; i++)
  {
      HostGuid[i] = '+';
      GuestGuid[i] = '-';
  }
  Arraylength =0;
  IR.Init(pinRecv);
}

void loop()
{
  if (ConToHost == false)
  {
    //handshake loop    
    if (Serial.available())
    {
      SerRecieve();
      switch (InitStep)
      {
        case 0:
          CheckForHostInit();
          break;
        case 1:
          GetHostGuid();
          break;
        default:
          break;
      }
    }
  }
  else
  {    
    //the real chat loop 
    SerRecieve();
    IRSend();  
    ClearSendRecBuffer();
    IRReceive();
    SerSend();
    ClearSendRecBuffer();
  }
}