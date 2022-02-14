#include <M5Stack.h>
#include <mcp_can.h>
#include <SPI.h>

int  serIn; //var that will hold the bytes in read from the serialBuffer
byte buffer1 [8] ;
long unsigned int rxId;
unsigned char len = 0;
unsigned char rxBuf[8];
int present_pos=0;
MCP_CAN CAN0(12);     // Set CS to pin 10

void setup() {
  Serial.begin(115200);
  if(CAN0.begin(CAN_1000KBPS) == CAN_OK) Serial.print("can init ok!!\r\n");
  else Serial.print("Can init fail!!\r\n");
 
}

void loop () {
 if(Serial.available()) { 
    while (Serial.available()>0){
      for (byte i = 0 ; i < 9 ; i++){
         buffer1[i]=Serial.read();         
     }   
     unsigned char newbuffer[8]={buffer1[1], buffer1[2], buffer1[3], buffer1[4], buffer1[5], buffer1[6] , buffer1[7], buffer1[8]};
     CAN0.sendMsgBuf(buffer1[0]+0x60, 0, 8, newbuffer); 
     delay(100);
     if (buffer1[1]==0x92){
      CAN0.readMsgBuf(&len, rxBuf);              // Read data: len = data length, buf = data byte(s)
      rxId = CAN0.getCanId();                    // Get message ID
      for(int i = 0; i<len; i++)                // Print each byte of the data
      {
        if(rxBuf[i] < 0x10)                     // If data byte is less than 0x10, add a leading zero
        {
         Serial.print("0");
        } 
      }
      //Serial.println();
      present_pos = rxBuf[1] + (rxBuf[2] << 8) + (rxBuf[3] << 16) + (rxBuf[4] << 24) + (rxBuf[5] << 32) + (rxBuf[6] << 48);
     int present_angle = present_pos * 0.01 / 6;
     Serial.println(present_angle);
     }
     }
    //the serial buffer is over just go to the line (or pass your favorite stop char)               
    M5.Lcd.println();
  }
  
  //slows down the visualization in the terminal
  delay(1000);
}
