/*
 * Author: Eduardo S. Pereira
 * Version: 0.1
 * Date: 30/03/2017
 */


#include "Arduino.h"


const int LM35 = A0;
float temperatura;
unsigned long t0 = millis();
unsigned long t1 = t0;


// Smooth Temp Data

const int readsSize = 30;
unsigned int readIndex = 0;
unsigned int reads[readsSize];

unsigned int totalReads;
unsigned int averageReads;

void smoothTemp(){
        totalReads = totalReads - reads[readIndex];

        reads[readIndex] = analogRead(LM35);

        totalReads = totalReads + reads[readIndex];
        readIndex += 1;
        if(readIndex >= readsSize) {
                readIndex = 0;
        }

        averageReads = totalReads / readsSize;

}

void setup(){
        Serial.begin(9600);
        for(int i = 0; i < readsSize; i++ ) {
                reads[i] = 0;
        }

}

void loop(){
        //temperatura = (float(analogRead(LM35)) * 5 / 1023) / 0.01;

        smoothTemp();

        temperatura = (float(averageReads) * 5 / 1023) / 0.01;

        if(millis() - t1 >= 1000) {
                t1 = millis();
                unsigned long t2 =  (t1 - t0) /  1000;
                Serial.print(t2, DEC);
                Serial.print(',');
                Serial.println(temperatura,DEC);
        }

}
