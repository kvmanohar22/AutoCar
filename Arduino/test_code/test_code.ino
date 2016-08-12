//assign the pin numbers
int left_pin = 6;
int right_pin = 7;
int forward_pin = 8;
int reverse_pin = 9;


void setup(){
	pinMode(left_pin, OUTPUT);
	pinMode(right_pin, OUTPUT);
	pinMode(forward_pin, OUTPUT);
	pinMode(reverse_pin, OUTPUT);
}


void loop(){
  
  /*
	//Test Case #1
	digitalWrite(forward_pin, HIGH);
	delay(1000);
	digitalWrite(forward_pin, LOW);
	delay(1000);

*/
	//Test Case #2

	digitalWrite(forward_pin, HIGH);
	delay(100);
	digitalWrite(forward_pin, LOW);	
	delay(100);
	digitalWrite(reverse_pin, HIGH);
	delay(100);
	digitalWrite(reverse_pin, LOW);
	delay(100);


}
