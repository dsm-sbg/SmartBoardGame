#include<Wire.h>
#include<SoftwareSerial.h>
SoftwareSerial mySerial(10, 11); // RX, TX

#define MPU6050 0x68 //MPU 6050 의 I2C 기본 주소 설정
#define X_ERROR 10
#define Y_ERROR 10
#define X_RANGE 10
#define Y_RANGE 10
#define COUNT_REFRESH 20
#define END_NUMBER 30
#define POWER_LED 13
#define WORK_LED 12
#define INTERRUPT 2

//------------------------------------------------------------------------------------------------------
int16_t AcX, AcY, AcZ;
int16_t AcZ_X=12700, AcZ_Y=12800;
int x_final, y_final;
int x_origin = 0, y_origin = 0;
int x_range = 0, y_range = 0;
int Save_Number = 0;
int Final_Number = 0;
int count_refresh = 0;
int count_number = 0;
uint8_t ud_flag;
uint8_t startdown_flag = 0;
uint8_t Start_Flag = 0;
char recived = 79;
//------------------------------------------------------------------------------------------------------
/*--User Define Funtion--*/
void mpu6050_Read(void);
void mpu6050_analysis(void);
int mpu6050_x_correction(double);
int mpu6050_y_correction(double);
void cube_startdown(void);
void cube_save_number(void);
void cube_final_number(void);
void Send_msg(void);
void user_delay(uint16_t);

void debug_print(void);
//------------------------------------------------------------------------------------------------------
void mpu6050_Read()
{
  Wire.beginTransmission(MPU6050);    //데이터 전송시작
  Wire.write(0x3B);               // register 0x3B (ACCEL_XOUT_H), 큐에 데이터 기록
  Wire.endTransmission(false);    //연결유지
  Wire.requestFrom(MPU6050,6,true);   //MPU에 데이터 요청 

  //데이터 한 바이트 씩 읽어서 반환
  AcX = Wire.read() << 8 | Wire.read();  // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)    
  AcY = Wire.read() << 8 | Wire.read();  // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  AcZ = Wire.read() << 8 | Wire.read();
}
//------------------------------------------------------------------------------------------------------
void mpu6050_analysis()
{
  double RADIAN_TO_DEGREES = 180/3.14;
  double x_vlaue = atan(AcY/sqrt(pow(AcX,2) + pow(AcZ_X,2))) * RADIAN_TO_DEGREES; //보정전 Roll값 구하기
  double y_vlaue = atan(AcX/sqrt(pow(AcY,2) + pow(AcZ_Y,2))) * RADIAN_TO_DEGREES; //보정전 Pitch값 구하기 
  x_final = mpu6050_x_correction(x_vlaue);
  y_final = mpu6050_y_correction(y_vlaue);

  if(AcZ < -15000)
  {
   ud_flag = 1; 
  }
  else
  {
    ud_flag = 0; 
  }
}
//------------------------------------------------------------------------------------------------------
int mpu6050_x_correction(double x_vlaue)
{
  x_vlaue = floor(x_vlaue+0.5);  //x_vlaue값 보정
  x_vlaue += 52;             //x_vlaue값의 음수값 삭제  

  double x_final = 90.0/104.0*x_vlaue;

  if(x_final == 45)
  {
    x_final = 0;
  }
  
  else if(x_final > 45)
  {
    if(x_final > 90)
    {
      x_final = -90;
    } 
    else
    {
      x_final -= 46; 
      x_final = 90.0/44.0*x_final;
      x_final *= -1;
    }
  }
  
  else if(x_final < 45)
  {
    if(x_final < 0)
    {
      x_final = 90;
    }
    else
    {
      x_final = 90.0/44.0*x_final-90;
      x_final *= -1;
    }
  }
   x_final = int(x_final);
   
   return x_final; 
}
//------------------------------------------------------------------------------------------------------
int mpu6050_y_correction(double y_vlaue)
{
  y_vlaue = floor(y_vlaue);  //y_vlaue값 보정
  y_vlaue += 52;         //y_vlaue값의 음수값 삭제

  double y_final = 90.0/104.0*y_vlaue;
  
  if(y_final == 45)
  {
    y_final = 0;
  }
  
  else if(y_final > 45)
  {
    if(y_final > 90)
    {
      y_final = 90;
    }

    else
    {
      y_final -= 46; 
      y_final = 90.0/44.0*y_final;
    }
  }
  
  else if(y_final < 45)
  {
    if(y_final < 0)
    {
      y_final = -90;
    }

    else
    {
      y_final = 90.0/44.0*y_final-90;
    }
  }
   y_final = floor(y_final);
   
   return y_final; 
}
//------------------------------------------------------------------------------------------------------
void cube_startdown()
{
  if(count_refresh == COUNT_REFRESH)
  {
    x_range = x_origin - x_final;
    y_range = y_origin - y_final;
    
    if(x_range < 0)
    {
      x_range *= -1;
    }
    if(y_range < 0)
    {
      y_range *= -1;
    }    

    if(x_range >= X_RANGE || y_range >= Y_RANGE)
    {
      digitalWrite(WORK_LED, LOW);
      startdown_flag = 1;
    }
    else
    {
      x_origin = x_final;
      y_origin = y_final;
    }
    count_refresh = 0;
  }
  else
  {
    count_refresh++;
  }
}
//------------------------------------------------------------------------------------------------------
void cube_save_number()
{
  if(ud_flag != 1)
  {
    if(x_final >= 90-X_ERROR && x_final <= 90+X_ERROR)
    {
      if(y_final >= 0-X_ERROR && y_final <= 0+X_ERROR)
      {
        Save_Number = 2;
      }
    }

    else if(x_final >= -90-X_ERROR && x_final <= -90+X_ERROR)
    {
      if(y_final >= 0-X_ERROR && y_final <= 0+X_ERROR)
      {
        Save_Number = 5;
      }
    }

    else if(x_final >= 0-X_ERROR && x_final <= 0+X_ERROR)
    {
      if(y_final >= 90-X_ERROR && y_final <= 90+X_ERROR)
      {
        Save_Number = 3;
      }
      
      else if(y_final >= -90-X_ERROR && y_final <= -90+X_ERROR)
      {
        Save_Number = 4;
      }

      else if(y_final >= 0-X_ERROR && y_final <= 0+X_ERROR)
      {
        Save_Number = 1;
      }
    }
  }
  else
  {
    Save_Number = 6;
  }
}
//------------------------------------------------------------------------------------------------------
void cube_final_number()
{
    if(Final_Number == Save_Number)
    {
      count_number++;
    }
    else
    {
      Final_Number = Save_Number;
      count_number = 0;
    }
  
   if(count_number == END_NUMBER)
   {
      if(Final_Number == 0)
      {
        Final_Number = 7;   
      }
      attachInterrupt(0, Recive_msg, RISING);
      Start_Flag = 0;
   } 
}
//------------------------------------------------------------------------------------------------------
void Recive_msg()
{
  detachInterrupt(0);
  SoftwareSerial mySerial(10, 11); // RX, TX
  mySerial.begin(115200);
  
  char temp;
  /*
  temp = mySerial.read();
  Serial.print("temp : "); Serial.println(temp);
  temp = mySerial.read();
  Serial.print("temp : "); Serial.println(temp);
  temp = mySerial.read();
  Serial.print("temp : "); Serial.println(temp);
  temp = mySerial.read();
  Serial.print("temp : "); Serial.println(temp);
    */
    
  Serial.println("ok");
  if(mySerial.available() > 0)
  {
    temp = mySerial.read();
    if(temp == 2)
    {
      Serial.println("good");
      recived = mySerial.read();
      temp = mySerial.read();
      if(temp != 3)
      {
        if(Final_Number == 0)
        {
          recived = 79;
        }
        else
        {
           recived = 80;
        }
      }
    }
  }
   
  if(recived == 80)
  {
    if(Final_Number == 0)
    {
      x_origin = x_final;
      y_origin = y_final; 
      digitalWrite(WORK_LED, HIGH);
      Start_Flag = 1;
    }  
  }
  else
  {
    attachInterrupt(0, Recive_msg, RISING);
  }
}
//------------------------------------------------------------------------------------------------------
void Send_msg()
{
  if(recived == 79)
  {
    Final_Number = 0;
    startdown_flag = 0;
    count_refresh = 0;
    count_number = 0;
    mySerial.write("\x02S\x03");
  }
  else if(recived == 80)
  {
      mySerial.write("\x02");
      mySerial.write(48+Final_Number);
      mySerial.write("\x03");
  }
  user_delay(200);
}
//------------------------------------------------------------------------------------------------------
void debug_print(void)
{
   //시리얼 모니터에 출력
  Serial.print("x_final = "); Serial.println(x_final);
  Serial.print("y_final = "); Serial.println(y_final);
  Serial.print("ud_flag = "); Serial.println(ud_flag);
  Serial.print("Save_Number = "); Serial.println(Save_Number);
  Serial.print("x_origin = "); Serial.println(x_origin);
  Serial.print("y_origin = "); Serial.println(y_origin);
  Serial.print("x_range = "); Serial.println(x_range);
  Serial.print("y_range = "); Serial.println(y_range);
  Serial.print("count_refresh = "); Serial.println(count_refresh);
  Serial.print("Final_Number = "); Serial.println(Final_Number);
  Serial.print("count_number = "); Serial.println(count_number);
  Serial.print("recived = "); Serial.println(recived);
  
  Serial.println(" ");
}
//------------------------------------------------------------------------------------------------------
//------------------------------------------------------------------------------------------------------
void setup()
{ 
  Wire.begin();      //Wire 라이브러리 초기화
  Wire.beginTransmission(MPU6050); //MPU로 데이터 전송 시작
  Wire.write(0x6B);  // PWR_MGMT_1 register
  Wire.write(0);     //MPU-6050 시작 모드로 만들기
  Wire.endTransmission(true);
  Serial.begin(115200);
  while (!Serial) 
  {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  mySerial.begin(115200);

  pinMode(POWER_LED, OUTPUT);
  pinMode(WORK_LED, OUTPUT);

  digitalWrite(POWER_LED, HIGH);
  digitalWrite(WORK_LED, LOW);

  pinMode(INTERRUPT, INPUT_PULLUP);
  //attachInterrupt(digitalPinToInterrupt(INTERRUPT), Recive_msg, RISING);
  attachInterrupt(0, Recive_msg, RISING);
}
//------------------------------------------------------------------------------------------------------
void user_delay(uint16_t ms_delay)
{
  volatile uint16_t i , j;
  ms_delay *= 100;
  for(i = 0; i <= ms_delay; i++)
    for(j = 0; j <= 8; j++);
}
//------------------------------------------------------------------------------------------------------
//------------------------------------------------------------------------------------------------------
void loop()
{   
  mpu6050_Read();
  mpu6050_analysis();
  if(Start_Flag == 1)
  {
    if(startdown_flag == 0)
    {
      cube_startdown();
    }
    else
    {
      cube_save_number();
      cube_final_number();
    }
  }
  else
  {
    Send_msg();
  } 
  //debug_print();
  user_delay(100);
}
