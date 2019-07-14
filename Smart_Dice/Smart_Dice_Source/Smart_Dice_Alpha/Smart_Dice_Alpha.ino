#include<Wire.h>
#include<SoftwareSerial.h>
SoftwareSerial mySerial(10, 11); // RX, TX

#define MPU6050 0x68 //MPU 6050 의 I2C 기본 주소 설정
#define X_ERROR 5
#define Y_ERROR 5

//------------------------------------------------------------------------------------------------------
int16_t AcX, AcY, AcZ;
int16_t AcZ_X=12700, AcZ_Y=12800;
int x_final, y_final;
int Save_Number = 0;
uint8_t ud_flag;
uint8_t Start_Flag = 0;
char recived = 79;
//------------------------------------------------------------------------------------------------------
/*--User Define Funtion--*/
void mpu6050_Read(void);
void mpu6050_analysis(void);
int mpu6050_x_correction(double);
int mpu6050_y_correction(double);
void cube_final_number(void);
void Send_msg(void);

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
void cube_final_number()
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

   Start_Flag = 0;
}
//------------------------------------------------------------------------------------------------------
void Send_msg()
{
  char* msg;
  char temp;
  if(recived == 79)
  {
    Save_Number=0;
    mySerial.write("\x02S\x03");
  }
  if(recived == 80)
  {
    Start_Flag=1;
    mySerial.write("\x02");
    mySerial.write(48+Save_Number);
    mySerial.write("\x03");
  }
  if(mySerial.available() > 0)
  {
      temp=mySerial.read();
      if(temp==2){
        recived = mySerial.read();
      }
  }
}
//------------------------------------------------------------------------------------------------------
void debug_print(void)
{
   //시리얼 모니터에 출력
  Serial.print("x_final:="); Serial.println(x_final);
  Serial.print("y_final:= "); Serial.println(y_final);
  Serial.print("ud_flag := "); Serial.println(ud_flag);
  Serial.print("Save_Number := "); Serial.println(Save_Number);
  Serial.print("recived := "); Serial.println(recived);
  
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
}
//------------------------------------------------------------------------------------------------------
//------------------------------------------------------------------------------------------------------
void loop()
{
  mpu6050_Read();
  mpu6050_analysis();
  if(Start_Flag == 1)
  {
    cube_final_number();
  }
  Send_msg();
  delay(300); 
  debug_print();
}
