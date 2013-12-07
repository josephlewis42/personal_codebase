#ifndef HMC_DRIVER_H
#define HMC_DRIVER_H

#include "i2c.h"

extern const unsigned char HMC6352_SLAVE_ADDRESS;
extern const unsigned char HMC6352_MAGNETOMETER_X_OFFSET_MSB;
extern const unsigned char HMC6352_MAGNETOMETER_X_OFFSET_LSB;
extern const unsigned char HMC6352_MAGNETOMETER_Y_OFFSET_MSB;
extern const unsigned char HMC6352_MAGNETOMETER_Y_OFFSET_LSB;
extern const unsigned char HMC6352_TIME_DELAY_MS;
extern const unsigned char HMC6352_NUM_SUMMED_MEASUREMENTS;
extern const unsigned char HMC6352_SOFTWARE_VERSION;
extern const unsigned char HMC6352_OPERATION_MODE;


unsigned char hmc6352_read_eeprom( i2c_p& i2c, unsigned char eeprom_addr );
void hmc6352_write_eeprom(i2c_p& i2c, unsigned char eeprom_address, unsigned char value);
unsigned char hmc6352_read_ram( i2c_p& i2c, unsigned char ram_addr );
void hmc6352_write_ram(i2c_p& i2c, unsigned char ram_addr, unsigned char value);
void hmc6352_start_user_calibration(i2c_p& i2c);
void hmc6352_stop_user_calibration(i2c_p& i2c);
unsigned int hmc6352_get_heading_degrees(i2c_p& i2c);
void hmc6352_calibrate_compass(i2c_p& i2c);

#endif
