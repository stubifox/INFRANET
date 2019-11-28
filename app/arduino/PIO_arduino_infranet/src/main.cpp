/*
 * Copyright (c) 2015 seeed technology inc.
 * Website    : www.seeed.cc
 * Author     : Seeed
 * Modified Time: July 2015
 * Description: Must connect the IR send pins to D3 for this demo. You can use Infrared Emitter combination with Infrared Receiver.
 *				You can see the remote control's infrared data that received through Infrared Receiver, then write the received 
 *				infrared data into send.ino and downloaded to the board with Infrared Emitter Grove, so you can send the same data  
 *				with remote control's button.
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
#include "Arduino.h"
#include <IRSendRev.h>

#define BIT_LEN 0
#define BIT_START_H 1
#define BIT_START_L 2
#define BIT_DATA_H 3
#define BIT_DATA_L 4
#define BIT_DATA_LEN 5
#define BIT_DATA 6
#define FREQUENCY 38 // 38kH
#define DATA_ARRAY_LEN 60
#define HEADER_LEN 6
#define DATA_LEN 50

const int ir_freq = FREQUENCY;

unsigned char dtaSend[DATA_ARRAY_LEN];

void dtaInit()
{
    dtaSend[BIT_LEN] = HEADER_LEN + DATA_LEN; // all data that needs to be sent
    dtaSend[BIT_START_H] = 179;               // the logic high duration of "Start"
    dtaSend[BIT_START_L] = 90;                // the logic low duration of "Start"
    dtaSend[BIT_DATA_H] = 11;                 // the logic "long" duration in the communication
    dtaSend[BIT_DATA_L] = 33;                 // the logic "short" duration in the communication

    dtaSend[BIT_DATA_LEN] = DATA_LEN; //number of data which will sent. If the number is other, you should increase or reduce dtaSend[BIT_DATA+x].
    //DATA WHICH IS SENT

    for (int i = 0; i < 50; i++)
    {
        dtaSend[BIT_DATA + i] = 96;
        Serial.println(i);
    }
}

void setup()
{
    dtaInit();
}

void loop()
{
    IR.Send(dtaSend, FREQUENCY);
    delay(2000);
}
