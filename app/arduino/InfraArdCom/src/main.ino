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
#define Arraylength 520

//variable from example : define the base frequenz
const int ir_freq = 38; // 38k

unsigned char SendRecBuffer[Arraylength];

// clearing the SendRecieve Buffer
void ClearSendRecBuffer()
{
  FlagsInit();
  SendRecBuffer[BIT_DATA] = '\n';
  for (int i = BIT_DATA + 1; i < Arraylength; i++)
  {
    SendRecBuffer[i] = ' ';
  }
}

void FlagsInit()
{
  SendRecBuffer[BIT_LEN] = 11;      // all data that needs to be sent
  SendRecBuffer[BIT_START_H] = 179; // the logic high duration of "Start"
  SendRecBuffer[BIT_START_L] = 90;  // the logic low duration of "Start"
  SendRecBuffer[BIT_DATA_H] = 11;   // the logic "long" duration in the communication
  SendRecBuffer[BIT_DATA_L] = 33;   // the logic "short" duration in the communication
  SendRecBuffer[BIT_HANDSHAKE] = 6;
}

// Send the Buffer to the host-computer using serial connection
void SerSend()
{
  if (SendRecBuffer[BIT_DATA] == '\n')
    return;
  for (int i = 0; i < Arraylength; i++)
  {
    Serial.write(SendRecBuffer[i]);
    if (SendRecBuffer[i] == '\n')
      return;
  }
  // if the buffer did not contain a newline, add it
  if (SendRecBuffer[Arraylength] != '\n')
    Serial.write('\n');
}

// Recieve Information from host-computer using serial and save it to the buffer
void SerRecieve()
{
  int i = BIT_DATA;
  while (Serial.available() && i < Arraylength)
  {
    SendRecBuffer[i] = Serial.read();
    if (SendRecBuffer[i] == '\n')
      break;
    i++;
    if (Serial.available() == false)
      delay(1);
  }
}

void IRReceive()
{
  if (IR.IsDta())
  {
    //IR.Recv(SendRecBuffer);
    SendRecBuffer[BIT_DATA] = 'K';
    SendRecBuffer[BIT_DATA+1] = 'R';    
    SendRecBuffer[BIT_DATA+2] = 'A';    
    SendRecBuffer[BIT_DATA+3] = 'S';    
    SendRecBuffer[BIT_DATA+4] = 'S';    
    SendRecBuffer[BIT_DATA+5] = '\n';    
  }
}

void setup()
{
  Serial.begin(115200);
  ClearSendRecBuffer();
}

void loop()
{
  SerRecieve();
  //IR.Send(SendRecBuffer, 38);
  IRReceive();
  SerSend();
  ClearSendRecBuffer();
}