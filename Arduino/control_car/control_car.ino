//assign the pin numbers
int left_pin = 6;
int right_pin = 7;
int forward_pin = 8;
int reverse_pin = 9;


//some initial commands 
int command = 0;
int time = 50;

//setup the modes of the pins
void setup() {
	pinMode(left_pin, OUTPUT);
	pinMode(right_pin, OUTPUT);
	pinMode(forward_pin, OUTPUT);
	pinMode(reverse_pin, OUTPUT);

	Serial.begin(115200);
	Serial.print("\nStarting.....\n");
}


void loop(){
  	
	//read the input from port
	if(Serial.available() > 0){
		command = Serial.read();
		Serial.print("Recieved: ");
		Serial.println(command);
	}
	else{
		reset();
                command = 48;
        }
	send_command(command);	
}

//single commands
void right(){
	Serial.println("Moving right...\n");
	digitalWrite(right_pin, HIGH);
	delay(time);
}

void left(){
	Serial.println("Moving left...\n");
	digitalWrite(left_pin, HIGH);
	delay(time);
}

void forward(){
	Serial.println("Moving forward...\n");
	digitalWrite(forward_pin, HIGH);
	delay(time);
}

void reverse(){
	Serial.println("Moving back...\n");
	digitalWrite(reverse_pin, HIGH);
	delay(time);
}

//complex commands
void forward_right(){
	Serial.println("Moving forward right...\n");
	digitalWrite(forward_pin, HIGH);
	digitalWrite(right_pin, HIGH);
        delay(1000);
	delay(time);
}

void forward_left(){
	Serial.println("Moving forward left...\n");
	digitalWrite(forward_pin, HIGH);
	digitalWrite(left_pin, HIGH);
	delay(time);
}

void reverse_right(){
	Serial.println("Moving Reverse right...\n");
	digitalWrite(reverse_pin, HIGH);
	digitalWrite(right_pin, HIGH);
	delay(time);
}

void reverse_left(){
	Serial.println("Moving Reverse left...\n");
	digitalWrite(reverse_pin, HIGH);
	digitalWrite(left_pin, HIGH);
	delay(time);
}


//reset 
void reset(){
	digitalWrite(forward_pin, LOW);
	digitalWrite(reverse_pin, LOW);
	digitalWrite(left_pin, LOW);
	digitalWrite(right_pin, LOW);
}

void send_command(int command){
	switch(command){
		//initial command
                //this is integer 0
		case 48: reset(); break;
		
		//single commands
                //1 represents 49
		case 49: forward(); break;
		case 50: reverse(); break;
		case 51: left(); break;
		case 52: right(); break;

		//complex commands
		case 53: forward_right(); break;
		case 54: forward_left(); break;
		case 55: reverse_right(); break;
		case 56: reverse_left(); break;
	
		//invalid
		default: Serial.print("Invalid command!\n");	
	}
}
