#include "IRSendRev.h"

//defines from example
#define BIT_LEN 0
#define BIT_START_H 1
#define BIT_START_L 2
#define BIT_DATA_H 3
#define BIT_DATA_L 4
#define BIT_HANDSHAKE 5
#define BIT_DATA 6

//own defines
int Arraylength;

//variable from example : define the base frequenz
const int ir_freq = 38; // 38k

const int pinRecv = 2; 

unsigned char SendRecBuffer[MaxMsgSize];

// clearing the SendRecieve Buffer
void ClearSendRecBuffer()
{
  Arraylength = 0;  
  FlagsInit();
  SendRecBuffer[BIT_DATA] = '\n';
  for (int i = BIT_DATA + 1; i < MaxMsgSize; i++)
  {
    SendRecBuffer[i] = ' ';
  }
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
  if (SendRecBuffer[BIT_DATA] == '\n')
    return;
  Serial.println("tried to send:");
  for (int i = BIT_DATA; i < MaxMsgSize; i++)
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
  int i = BIT_DATA;
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
  FlagsInit();
}

void IRSend()
{
  //IR.EnableIROut(ir_freq);
  if (SendRecBuffer[BIT_DATA] == '\n') return;
  IR.ImpSend(SendRecBuffer, 38);
  delay(1000);
  IR.ClearNew();
  IR.EnableIRIn();
}

void IRReceive()
{
  if(IR.ready)                  // get IR data
  {
  if ((IR.start_l < 50 && IR.start_h > 0) || (IR.start_h < 50 && IR.start_h > 0) || IR.MessageCharCount == 0)
  {
    IR.ClearNew();
    return;
  }
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
      for (int i=0; i<MaxMsgSize; i++)
      {
        Serial.write(IR.SendReceiveBuffer[i]);
      }
    Serial.println("\nend");
    IR.ClearNew();
  }
}

void setup()
{
  Arraylength =0;
  Serial.begin(115200);
  IR.Init(pinRecv);
  ClearSendRecBuffer();
}

void loop()
{
  SerRecieve();
  IRSend();
  IRReceive();
  SerSend();
  ClearSendRecBuffer();
}