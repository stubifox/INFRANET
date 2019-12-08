/*
 * Copyright (c) 2015 seeed technology inc.
 * Website    : www.seeed.cc
 * Author     : Seeed
 * Modified Time: July 2015
 * Description: Connect the IR receiver pins to D2 for this demo. You can see the remote control's infrared data 
 *   			that received through a serial port terminal, then write the received infrared data into send.ino 
 *				and downloaded to the board with Infrared Emitter Grove, so you can send the same data with 
 *				remote control's button.
 * 
 * The MIT License (MIT)
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

#include <IRSendRev.h>

#define BIT_LEN         0
#define BIT_START_H     1
#define BIT_START_L     2
#define BIT_DATA_H      3
#define BIT_DATA_L      4
#define BIT_DATA_LEN    5
#define BIT_DATA        6

const int pinRecv = 2;              // ir receiver connect to D2

void setup()
{
    Serial.begin(115200);
    IR.Init(pinRecv);
    Serial.println("init over");
}

unsigned char dta[52];

void loop()
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