/*
 * @author Kai Fischer
 * @email kathunfischer@googlemail.com
 * @desc definition of the used classes, implementation in "IRSendRev.cpp"
 * 
 * @info    this is a modified version of the original "https://github.com/Seeed-Studio/IRSendRev/blob/master/IRSendRev.h"
 *          to fit the needs of the InfranetProjekt, like other send and recieve methods
 *          all modified parts are marked: search for "modified"
 */

#ifndef _IRSENDREV_H_
#define _IRSENDREV_H_

// len, start_H, start_L, nshort, nlong, data_len, data[data_len]....
#define D_LEN 0
#define D_STARTH 1
#define D_STARTL 2
#define D_SHORT 3
#define D_LONG 4
#define D_DATALEN 5
#define D_DATA 6

#define n_short = 11

#define USECPERTICK 50 // microseconds per clock interrupt tick

// modified:
#define MaxMsgSize 520
// end modified

// Marks tend to be 100us too long, and spaces 100us too short
// when received due to sensor lag.
#define MARK_EXCESS 100

#define __DEBUG 0

// Results returned from the decoder
class decode_results
{

public:
    volatile unsigned int *rawbuf; // Raw intervals in .5 us ticks
    int rawlen;                    // Number of records in rawbuf.
};

// main class for receiving IR
class IRSendRev
{
private:
    decode_results results;
    //**************************rev**********************************

private:
    int decode(decode_results *results);

// modified:
public:
    volatile bool ready;
    volatile unsigned char start_h;
    volatile unsigned char start_l;
    volatile unsigned char first;
    volatile unsigned char short_time;
    volatile unsigned char long_time;
    volatile unsigned char SendReceiveBuffer[MaxMsgSize];
    volatile unsigned int MessageCharCount;
    volatile unsigned char IRBuffer[16];
    volatile int IRBufferCounter;
    void Init(int revPin); // init
    void Init();
    void ClearNew();
    void ValidateOrThrowInput();
    unsigned char Recv(unsigned char *revData); //
    unsigned char IsDta();                      // if IR get data
    //void Clear();                               // clear IR data
    void ClearSRBuffer();
    //**************************send*********************************
private:
    void ImpSendRaw(unsigned int time, bool *toggleFlag);
    void sendRaw(unsigned int buf[], int len, int hz);

    // private:

    void mark(int usec);
    void space(int usec);


public:
    void ImpSend(unsigned char *idata, unsigned char ifreq);
    void Send(unsigned char *idata, unsigned char ifreq);
    void EnableIROut(int khz);
    void EnableIRIn();
// end modified
};

extern IRSendRev IR;

#endif
