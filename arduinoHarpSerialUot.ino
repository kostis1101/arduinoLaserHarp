/*
 *      |     | array 
 * note | pin | index
 * ==================
 * C  ->  A1     (0)
 * Cs ->  A2     (1)
 * D  ->  A3     (2)
 * Ds ->  A4     (3)
 * E  ->  A5     (4)
 * F  ->  A6     (5)
 * Fs ->  A7     (6)
 * G  ->  A8     (7)
 * Gs ->  A9     (8)
 * A  ->  A10    (9)
 * As ->  A11    (10)
 * B  ->  A12    (11)
 */

int notePins[] = {A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13};
int lastNotesInput[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
int notesInput[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
int output[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

int lightThresshold = 50;

void setup() {
  Serial.begin(9600);
  for (int pin = 0; pin < 12; pin++)
  {
    pinMode(notePins[pin], INPUT);
  }
}

void loop() {

  for (int n = 0; n < 12; n++)
  {
    int correntNoteInput = 0;
    correntNoteInput = analogRead(notePins[n]);
    notesInput[n] = correntNoteInput;

    if(correntNoteInput >= lightThresshold && lastNotesInput[n] < lightThresshold)
    {
      output[n] = -1;
    }
    else if((correntNoteInput >= lightThresshold && lastNotesInput[n] >= lightThresshold) || (correntNoteInput < lightThresshold && lastNotesInput[n] < lightThresshold))
    {
      output[n] = 0;
    }
    else if(correntNoteInput < lightThresshold && lastNotesInput[n] >= lightThresshold)
    {
      output[n] = 1;
    }
  }

  String toPrint = "";

  for (int out : output)
  {
    toPrint += String(out) + ",";
  }

  Serial.println(toPrint);

  for (int n = 0; n < 12; n++)
  {
    lastNotesInput[n] = notesInput[n];
  }

  
  /* logic for each note
  
  if(input >= lightThresshold && lastIn < lightThresshold)
  {
    Serial.println(-1);
  }
  else if((input >= lightThresshold && lastIn >= lightThresshold) || (input < lightThresshold && lastIn < lightThresshold))
  {
    Serial.println(0);
  }
  else if(input < lightThresshold && lastIn >= lightThresshold)
  {
    Serial.println(1);
  }
  */
}
