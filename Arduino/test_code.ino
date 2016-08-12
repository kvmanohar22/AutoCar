//assign the pin numbers
int left_pin;
int right_pin;
int forward_pin;
int reverse_pin;


void setup(){
	pinMode(left_pin, OUTPUT);
	pinMode(right_pin, OUTPUT);
	pinMode(forward_pin, OUTPUT);
	pinMode(reverse_pin, OUTPUT);
}


void loop(){
	//Test Case #1
	digitalWrite(forward_pin, HIGH);
	delay(2000);
	digitalWrite(reverse_pin, LOW);
	delay(2000);

	//Test Case #2
	digitalWrite(forward_pin, HIGH);
	delay(2000);
	digitalWrite(forward_pin, LOW);	
	delay(2000);
	digitalWrite(reverse_pin, HIGH);
	delay(2000);
	digitalWrite(reverse_pin, LOW);
	delay(2000);
}
