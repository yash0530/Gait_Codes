#include <ESP8266WiFi.h>
#include <Wire.h>

//--------------MPU6050-----------------------//

void MPU6050_Init();
void Read_RawValue(uint8_t deviceAddress, uint8_t regAddress);
void I2C_Write(uint8_t deviceAddress, uint8_t regAddress, uint8_t data);

// MPU6050 Slave Device Address
const uint8_t MPU6050SlaveAddress = 0x68;

// Select SDA and SCL pins for I2C communication 
const uint8_t scl = D15;
const uint8_t sda = D14;

// sensitivity scale factor respective to full scale setting provided in datasheet 
const uint16_t AccelScaleFactor = 16384;
const uint16_t GyroScaleFactor = 131;

// MPU6050 few configuration register addresses
const uint8_t MPU6050_REGISTER_SMPLRT_DIV   =  0x19;
const uint8_t MPU6050_REGISTER_USER_CTRL    =  0x6A;
const uint8_t MPU6050_REGISTER_PWR_MGMT_1   =  0x6B;
const uint8_t MPU6050_REGISTER_PWR_MGMT_2   =  0x6C;
const uint8_t MPU6050_REGISTER_CONFIG       =  0x1A;
const uint8_t MPU6050_REGISTER_GYRO_CONFIG  =  0x1B;
const uint8_t MPU6050_REGISTER_ACCEL_CONFIG =  0x1C;
const uint8_t MPU6050_REGISTER_FIFO_EN      =  0x23;
const uint8_t MPU6050_REGISTER_INT_ENABLE   =  0x38;
const uint8_t MPU6050_REGISTER_ACCEL_XOUT_H =  0x3B;
const uint8_t MPU6050_REGISTER_SIGNAL_PATH_RESET  = 0x68;

int16_t AccelX, AccelY, AccelZ, Temperature, GyroX, GyroY, GyroZ;


//----------------ESP8266---------------------//

const char* ssid     = "DSP"; //Wi-Fi SSID
const char* password = "saiprasadduduka"; //Wi-Fi Password

//Only used if using Static IP
IPAddress ip(192, 168, 43, 1); //IP
IPAddress gatewayDNS(192, 168, 43, 1);//DNS and Gewateway
IPAddress netmask(255, 255, 255,0); //Netmask

//Server IP or domain name
const char* host = "192.168.43.137";


//--------------------------------------------------------------//



void setup() {

  //----------------MPU6050-----------------------------//

  Serial.begin(115200);
  Wire.begin(sda, scl);
  MPU6050_Init();

  //----------------ESP8266-----------------------------//
  
  delay(10);

  // We start by connecting to a WiFi network

  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.config(ip,gatewayDNS,netmask,gatewayDNS); //Only used if using Static IP 
  WiFi.begin(ssid, password); //Connecting to the network
  
  while (WiFi.status() != WL_CONNECTED) { //Wait till connects
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP()); //Use if using DHCP to know the IP
}

//---------------------------------------------------//

float gx= 0,gy = 0,gz =0;

void loop() {

  //----------------MPU6050-----------------------------//
  
  double Ax, Ay, Az, T, Gx, Gy, Gz;
  
  Read_RawValue(MPU6050SlaveAddress, MPU6050_REGISTER_ACCEL_XOUT_H);
  
  //divide each with their sensitivity scale factor
  Ax = (double)AccelX/AccelScaleFactor;
  Ay = (double)AccelY/AccelScaleFactor;
  Az = (double)AccelZ/AccelScaleFactor;
  T = (double)Temperature/340+36.53; //temperature formula
  Gx = (double)GyroX/GyroScaleFactor;
  Gy = (double)GyroY/GyroScaleFactor;
  Gz = (double)GyroZ/GyroScaleFactor;

  delay(35);

  //---------filtering acceleartion readings--------------//
  gx = 0.9 * gx + 0.1*Ax;//gFil = (1 - alpha)*gRaw + alpha*rawAcce)
  gy = 0.9 * gy + 0.1*Ay;
  gz = 0.89 * gz + 0.11*Az;

  Ax = Ax - gx;
  float Tx = millis();
  Ay = Ay - gy;
  float Ty = millis();
  Az = Az - gz;
  float Tz = millis();

  //----------Printing-----------------------//
  Serial.print("Ax: "); Serial.print(Ax);
  Serial.print(" Ay: "); Serial.print(Ay);
  Serial.print(" Az: "); Serial.print(Az);
  Serial.print(" Gx: "); Serial.print(Gx);
  Serial.print(" Gy: "); Serial.print(Gy);
  Serial.print(" Gz: "); Serial.println(Gz);

  Serial.print(" Tx: "); Serial.print(Tx);
  Serial.print(" Ty: "); Serial.print(Ty);
  Serial.print(" Tz: "); Serial.print(Tz);

  //----------------ESP8266-----------------------------//

  Serial.print("connecting to ");
  Serial.println(host);
  WiFiClient client; //Client to handle TCP Connection
    const int httpPort = 80;
    if (!client.connect(host, httpPort)) { //Connect to server using port httpPort
      Serial.println("connection failed");
      return;
    }
    else {
      Serial.println("connected to server");
      // This will send the request to the server
      client.print("GET /esp/PHP%20code/write_data.php?");
      client.print("aX=");
      client.print(Ax);
      client.print("&aY=");
      client.print(Ay);
      client.print("&aZ=");
      client.print(Az);
      client.print("&gX=");
      client.print(Gx);
      client.print("&gY=");
      client.print(Gy);
      client.print("&gZ=");
      client.print(Gz);
      client.print("&time=");
      client.print(Tx);
      client.println(" HTTP/1.1");
      client.println("Host: 192.168.43.137");
      client.println("Connection: close");
      client.println();
      client.println();
      Serial.println("uploaded");
      client.stop();
    }
}

//--------------------------MPU6050----------------------------//

void I2C_Write(uint8_t deviceAddress, uint8_t regAddress, uint8_t data){
  Wire.beginTransmission(deviceAddress);
  Wire.write(regAddress);
  Wire.write(data);
  Wire.endTransmission();
}

// read all 14 register
void Read_RawValue(uint8_t deviceAddress, uint8_t regAddress){
  Wire.beginTransmission(deviceAddress);
  Wire.write(regAddress);
  Wire.endTransmission();
  Wire.requestFrom(deviceAddress, (uint8_t)14);
  AccelX = (((int16_t)Wire.read()<<8) | Wire.read());
  AccelY = (((int16_t)Wire.read()<<8) | Wire.read());
  AccelZ = (((int16_t)Wire.read()<<8) | Wire.read());
  Temperature = (((int16_t)Wire.read()<<8) | Wire.read());
  GyroX = (((int16_t)Wire.read()<<8) | Wire.read());
  GyroY = (((int16_t)Wire.read()<<8) | Wire.read());
  GyroZ = (((int16_t)Wire.read()<<8) | Wire.read());
}

//configure MPU6050
void MPU6050_Init(){
  delay(150);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_SMPLRT_DIV, 0x07);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_PWR_MGMT_1, 0x01);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_PWR_MGMT_2, 0x00);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_CONFIG, 0x00);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_GYRO_CONFIG, 0x00);//set +/-250 degree/second full scale
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_ACCEL_CONFIG, 0x00);// set +/- 2g full scale
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_FIFO_EN, 0x00);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_INT_ENABLE, 0x01);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_SIGNAL_PATH_RESET, 0x00);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_USER_CTRL, 0x00);
}
