#ifndef HMC6352_H_
#define HMC6352_H_

#include "i2c.h"

typedef enum {
	SLAVE_ADDRESS=0,
	MAGNETOMETER_X_OFFSET_MSB=1,
	MAGNETOMETER_X_OFFSET_LSB=2,
	MAGNETOMETER_Y_OFFSET_MSB=3,
	MAGNETOMETER_Y_OFFSET_LSB=4,
	TIME_DELAY=5,
	NUM_SUMMED_MEASUREMENTS=6,
	SOFTWARE_VERSION_NUMBER=7,
	OPERATION_MODE=8
} hmc6352_eeprom_address_t;

unsigned int hmc6352_get_heading_degrees(i2c_p& i2c);

unsigned char hmc6352_read_eeprom(i2c_p& i2c,
		hmc6352_eeprom_address_t eeprom_address);

unsigned char hmc6352_read_ram(i2c_p& i2c, unsigned char ram_address);
void hmc6352_start_user_calibration(i2c_p& i2c);
void hmc6352_stop_user_calibration(i2c_p& i2c);
void hmc6352_write_eeprom( i2c_p& i2c,
		hmc6352_eeprom_address_t eeprom_address, unsigned char value);
void hmc6352_write_ram( i2c_p& i2c, unsigned char ram_address, unsigned char value);
unsigned int hmc6352_get_heading_tenth_degrees(i2c_p& i2c);

#endif /* HMC6352_H_ */
