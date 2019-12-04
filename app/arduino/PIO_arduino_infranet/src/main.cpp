#include <Arduino.h>
#define MsgLength 512
#define GuidLength 36
unsigned char SendRecBuffer[MsgLength];
bool ConToHost;
unsigned char HostGuid[GuidLength];
unsigned char GuestGuid[GuidLength];
int InitStep;

// clearing the SendRecieve Buffer
void ClearSendRecBuffer()
{
    SendRecBuffer[0] = '\n';
    for (int i = 1; i < MsgLength; i++)
    {
        SendRecBuffer[i] = '_';
    }
}

/*// Send the Buffer to the host-computer using serial connection
void SerSend(){
  for (int i=0; i<MsgLength; i++){
    Serial.write(SendRecBuffer[i]);
    if (SendRecBuffer[i] == '\n') break;
  }
  ClearSendRecBuffer();
  
}*/

// Recieve Information from host-computer using serial and save it to the buffer
void SerRecieve()
{
    int i = 0;
    while (Serial.available() && i < MsgLength)
    {
        SendRecBuffer[i] = Serial.read();
        if (SendRecBuffer[i] == '\n')
            break;
        i++;
    }
}

void EchoAll()
{
    if (SendRecBuffer[0] != '\n')
    {
        for (int i = 0; i < MsgLength; i++)
        {
            Serial.write(SendRecBuffer[i]);
            if (SendRecBuffer[i] == '\n')
                return;
        }
        Serial.write('\n');
    }
}

void CheckForHostInit()
{
    char PingInput[] = "~echo~\n";
    char PingOutput[] = "~ping~\n";

    // wait for correct Ping input request
    for (int i = 0; i < 7; i++)
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

void GetHostGuid()
{
    char GotGuidMsg[] = "~okay~\n";

    // save the Guid from Host
    for (int i = 0; i < GuidLength; i++)
    {
        HostGuid[i] = SendRecBuffer[i];
    }

    // confirm got guid
    Serial.write(GotGuidMsg);
    ConToHost = true;
    InitStep = 2;
}

void setup()
{
    Serial.begin(115200);
    ConToHost = false;
    ClearSendRecBuffer();
    InitStep = 0;
    for (int i = 0; i < GuidLength; i++)
    {
        HostGuid[i] = '+';
        GuestGuid[i] = '-';
    }
}

void loop()
{
    if (Serial.available())
    {
        SerRecieve();
        if (ConToHost == false)
        {
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
        else
        {
            EchoAll();
        }
    }
    delay(10);
}
