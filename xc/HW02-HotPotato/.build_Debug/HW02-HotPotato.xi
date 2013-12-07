# 1 "../src/HW02-HotPotato.xc"
# 1 "stdio.h" 1 3
# 29 "stdio.h" 3
# 1 "_ansi.h" 1 3
# 15 "_ansi.h" 3
# 1 "newlib.h" 1 3
# 16 "_ansi.h" 2 3
# 1 "sys/config.h" 1 3
# 4 "sys/config.h" 3
# 1 "machine/ieeefp.h" 1 3
# 5 "sys/config.h" 2 3
# 17 "_ansi.h" 2 3
# 30 "stdio.h" 2 3
# 34 "stdio.h" 3
# 1 "stddef.h" 1 3
# 214 "stddef.h" 3
typedef  unsigned int  size_t;
# 35 "stdio.h" 2 3
# 51 "stdio.h" 3
# 1 "sys/types.h" 1 3
# 20 "sys/types.h" 3
# 1 "_ansi.h" 1 3
# 21 "sys/types.h" 2 3
# 25 "sys/types.h" 3
# 1 "machine/_types.h" 1 3
# 7 "machine/_types.h" 3
# 1 "machine/_default_types.h" 1 3
# 22 "machine/_default_types.h" 3
# 1 "limits.h" 1 3
# 4 "limits.h" 3
# 1 "newlib.h" 1 3
# 5 "limits.h" 2 3
# 24 "limits.h" 3
# 1 "sys/config.h" 1 3
# 25 "limits.h" 2 3
# 23 "machine/_default_types.h" 2 3



typedef signed char __int8_t ;
typedef unsigned char __uint8_t ;








typedef signed short __int16_t;
typedef unsigned short __uint16_t;
# 46 "machine/_default_types.h" 3
typedef __int16_t __int_least16_t;
typedef __uint16_t __uint_least16_t;
# 58 "machine/_default_types.h" 3
typedef signed int __int32_t;
typedef unsigned int __uint32_t;
# 76 "machine/_default_types.h" 3
typedef __int32_t __int_least32_t;
typedef __uint32_t __uint_least32_t;
# 8 "machine/_types.h" 2 3
# 26 "sys/types.h" 2 3
# 61 "sys/types.h" 3
# 1 "sys/_types.h" 1 3
# 12 "sys/_types.h" 3
# 1 "machine/_types.h" 1 3
# 13 "sys/_types.h" 2 3
# 1 "sys/lock.h" 1 3



typedef int _LOCK_T;
typedef struct {
  int _owner;
  int _count;
} _LOCK_RECURSIVE_T;
# 14 "sys/_types.h" 2 3


typedef long _off_t;







typedef short __dev_t;




typedef unsigned short __uid_t;


typedef unsigned short __gid_t;
# 45 "sys/_types.h" 3
typedef long _fpos_t;
# 57 "sys/_types.h" 3
typedef int _ssize_t;
# 64 "sys/_types.h" 3
# 1 "stddef.h" 1 3
# 355 "stddef.h" 3
typedef  unsigned int  wint_t;
# 65 "sys/_types.h" 2 3



typedef struct
{
  int __count;
  union
  {
    wint_t __wch;
    unsigned char __wchb[4];
  } __value;
} _mbstate_t;



typedef _LOCK_RECURSIVE_T _flock_t;
# 62 "sys/types.h" 2 3
# 69 "sys/types.h" 3
# 1 "stddef.h" 1 3
# 152 "stddef.h" 3
typedef  int  ptrdiff_t;
# 326 "stddef.h" 3
typedef  unsigned char  wchar_t;
# 70 "sys/types.h" 2 3
# 1 "machine/types.h" 1 3
# 19 "machine/types.h" 3
typedef long int __off_t;
typedef int __pid_t;



typedef long int __loff_t;
# 71 "sys/types.h" 2 3
# 92 "sys/types.h" 3
typedef unsigned char u_char;
typedef unsigned short u_short;
typedef unsigned int u_int;
typedef unsigned long u_long;



typedef unsigned short ushort;
typedef unsigned int uint;



typedef  unsigned long  clock_t;




typedef  long  time_t;




struct timespec {
  time_t tv_sec;
  long tv_nsec;
};

struct itimerspec {
  struct timespec it_interval;
  struct timespec it_value;
};


typedef long daddr_t;
# 135 "sys/types.h" 3
typedef unsigned short ino_t;
# 164 "sys/types.h" 3
typedef _off_t off_t;
typedef __dev_t dev_t;
typedef __uid_t uid_t;
typedef __gid_t gid_t;


typedef int pid_t;

typedef long key_t;

typedef _ssize_t ssize_t;
# 188 "sys/types.h" 3
typedef unsigned int mode_t  ;




typedef unsigned short nlink_t;
# 215 "sys/types.h" 3
typedef long fd_mask;
# 223 "sys/types.h" 3
typedef struct _types_fd_set {
	fd_mask fds_bits[ ((( 64 )+(( (sizeof (fd_mask) * 8 ) )-1))/( (sizeof (fd_mask) * 8 ) )) ];
} _types_fd_set;
# 246 "sys/types.h" 3
typedef  unsigned long  clockid_t;




typedef  unsigned long  timer_t;



typedef unsigned long useconds_t;
typedef long suseconds_t;
# 258 "sys/types.h" 3
# 1 "sys/features.h" 1 3
# 259 "sys/types.h" 2 3
# 52 "stdio.h" 2 3


# 183 "stdio.h" 3
int  printf (const char format[], ...) ;
# 185 "stdio.h" 3
int  scanf (const char format[], ...) ;
# 187 "stdio.h" 3
int  sscanf (const char str[], const char format[], ...) ;
# 202 "stdio.h" 3
int  getchar (void) ;
# 207 "stdio.h" 3
int  putchar (int) ;
int  puts (const char _s[]) ;
# 230 "stdio.h" 3
void  perror (const char _s[]) ;
# 234 "stdio.h" 3
int  sprintf (char str[], const char format[], ...) ;
# 236 "stdio.h" 3
int  remove (const char _file[]) ;
int  rename (const char _from[], const char _to[]) ;
# 257 "stdio.h" 3
int  diprintf (int, const char format[], ...) ;
# 260 "stdio.h" 3
int  fcloseall ( void ) ;
# 267 "stdio.h" 3
int  iprintf (const char format[], ...) ;
# 269 "stdio.h" 3
int  iscanf (const char format[], ...) ;
# 271 "stdio.h" 3
int  siprintf (char str[], const char format[], ...) ;
# 273 "stdio.h" 3
int  siscanf (const char str[], const char format[], ...) ;
# 275 "stdio.h" 3
int  snprintf (char str[], size_t, const char format[], ...) ;
# 277 "stdio.h" 3
int  sniprintf (char str[], size_t, const char format[], ...) ;
# 610 "stdio.h" 3

# 2 "../src/HW02-HotPotato.xc" 2
# 1 "print.h" 1 3
# 34 "print.h" 3
int printchar(char value);
# 40 "print.h" 3
int printcharln(char value);
# 46 "print.h" 3
int printint(int value);
# 52 "print.h" 3
int printintln(int value);
# 58 "print.h" 3
int printuint(unsigned value);
# 64 "print.h" 3
int printuintln(unsigned value);
# 71 "print.h" 3
int printhex(unsigned value);
# 78 "print.h" 3
int printhexln(unsigned value);
# 84 "print.h" 3
int printstr(const char s[]);
# 90 "print.h" 3
int printstrln(const char s[]);
# 3 "../src/HW02-HotPotato.xc" 2
# 1 "platform.h" 1 3
# 21 "platform.h" 3
# 1 "/home/joseph/School/comp/joslewis/HW02-HotPotato/.build_Debug/XK-1A.h" 1
# 4 "/home/joseph/School/comp/joslewis/HW02-HotPotato/.build_Debug/XK-1A.h"
# 1 "xs1.h" 1 3
# 31 "xs1.h" 3
# 1 "xs1_g4000b-512.h" 1 3
# 32 "xs1.h" 2 3
# 37 "xs1.h" 3
# 1 "xs1_user.h" 1 3
# 20 "xs1_user.h" 3
# 1 "xs1b_user.h" 1 3
# 21 "xs1_user.h" 2 3
# 38 "xs1.h" 2 3
# 1 "xs1_kernel.h" 1 3
# 20 "xs1_kernel.h" 3
# 1 "xs1b_kernel.h" 1 3
# 21 "xs1_kernel.h" 2 3
# 39 "xs1.h" 2 3
# 1 "xs1_registers.h" 1 3
# 20 "xs1_registers.h" 3
# 1 "xs1b_registers.h" 1 3
# 29 "xs1b_registers.h" 3
# 1 "xs1_g_registers.h" 1 3
# 30 "xs1b_registers.h" 2 3
# 1 "xs1_l_registers.h" 1 3
# 31 "xs1b_registers.h" 2 3
# 21 "xs1_registers.h" 2 3
# 40 "xs1.h" 2 3
# 94 "xs1.h" 3
void configure_in_port_handshake(void port p, in port readyin,
                                 out port readyout,  __clock_t  clk);
# 123 "xs1.h" 3
void configure_out_port_handshake(void port p, in port readyin,
                                 out port readyout,  __clock_t  clk,
                                 unsigned initial);
# 149 "xs1.h" 3
void configure_in_port_strobed_master(void port p, out port readyout,
                                      const  __clock_t  clk);
# 172 "xs1.h" 3
void configure_out_port_strobed_master(void port p, out port readyout,
                                      const  __clock_t  clk, unsigned initial);
# 194 "xs1.h" 3
void configure_in_port_strobed_slave(void port p, in port readyin,  __clock_t  clk);
# 219 "xs1.h" 3
void configure_out_port_strobed_slave(void port p, in port readyin,  __clock_t  clk,
                                      unsigned initial);
# 243 "xs1.h" 3
void configure_in_port(void port p, const  __clock_t  clk);
# 249 "xs1.h" 3
void configure_in_port_no_ready(void port p, const  __clock_t  clk);
# 272 "xs1.h" 3
void configure_out_port(void port p, const  __clock_t  clk, unsigned initial);
# 278 "xs1.h" 3
void configure_out_port_no_ready(void port p, const  __clock_t  clk, unsigned initial);
# 288 "xs1.h" 3
void configure_port_clock_output(void port p, const  __clock_t  clk);
# 297 "xs1.h" 3
void start_port(void port p);
# 304 "xs1.h" 3
void stop_port(void port p);
# 317 "xs1.h" 3
void configure_clock_src( __clock_t  clk, void port p);
# 331 "xs1.h" 3
void configure_clock_ref( __clock_t  clk, unsigned char divide);
# 347 "xs1.h" 3
void configure_clock_rate( __clock_t  clk, unsigned a, unsigned b);
# 361 "xs1.h" 3
void configure_clock_rate_at_least( __clock_t  clk, unsigned a, unsigned b);
# 375 "xs1.h" 3
void configure_clock_rate_at_most( __clock_t  clk, unsigned a, unsigned b);
# 388 "xs1.h" 3
void set_clock_src( __clock_t  clk, void port p);
# 401 "xs1.h" 3
void set_clock_ref( __clock_t  clk);
# 417 "xs1.h" 3
void set_clock_div( __clock_t  clk, unsigned char div);
# 432 "xs1.h" 3
void set_clock_rise_delay( __clock_t  clk, unsigned n);
# 447 "xs1.h" 3
void set_clock_fall_delay( __clock_t  clk, unsigned n);
# 467 "xs1.h" 3
void set_port_clock(void port p, const  __clock_t  clk);
# 485 "xs1.h" 3
void set_port_ready_src(void port p, void port ready);
# 503 "xs1.h" 3
void set_clock_ready_src( __clock_t  clk, void port ready);
# 513 "xs1.h" 3
void set_clock_on( __clock_t  clk);
# 523 "xs1.h" 3
void set_clock_off( __clock_t  clk);
# 533 "xs1.h" 3
void start_clock( __clock_t  clk);
# 541 "xs1.h" 3
void stop_clock( __clock_t  clk);
# 551 "xs1.h" 3
void set_port_use_on(void port p);
# 561 "xs1.h" 3
void set_port_use_off(void port p);
# 571 "xs1.h" 3
void set_port_mode_data(void port p);
# 583 "xs1.h" 3
void set_port_mode_clock(void port p);
# 604 "xs1.h" 3
void set_port_mode_ready(void port p);
# 615 "xs1.h" 3
void set_port_drive(void port p);
# 631 "xs1.h" 3
void set_port_drive_low(void port p);
# 646 "xs1.h" 3
void set_port_pull_up(void port p);
# 661 "xs1.h" 3
void set_port_pull_down(void port p);
# 671 "xs1.h" 3
void set_port_pull_none(void port p);
# 685 "xs1.h" 3
void set_port_master(void port p);
# 699 "xs1.h" 3
void set_port_slave(void port p);
# 713 "xs1.h" 3
void set_port_no_ready(void port p);
# 728 "xs1.h" 3
void set_port_strobed(void port p);
# 741 "xs1.h" 3
void set_port_handshake(void port p);
# 750 "xs1.h" 3
void set_port_no_sample_delay(void port p);
# 759 "xs1.h" 3
void set_port_sample_delay(void port p);
# 767 "xs1.h" 3
void set_port_no_inv(void port p);
# 778 "xs1.h" 3
void set_port_inv(void port p);
# 801 "xs1.h" 3
void set_port_shift_count( void port p, unsigned n);
# 816 "xs1.h" 3
void set_pad_delay(void port p, unsigned n);
# 831 "xs1.h" 3
void set_thread_fast_mode_on(void);
# 839 "xs1.h" 3
void set_thread_fast_mode_off(void);
# 865 "xs1.h" 3
void start_streaming_slave(chanend c);
# 884 "xs1.h" 3
void start_streaming_master(chanend c);
# 897 "xs1.h" 3
void stop_streaming_slave(chanend c);
# 910 "xs1.h" 3
void stop_streaming_master(chanend c);
# 925 "xs1.h" 3
void outuchar(chanend c, unsigned char val);
# 940 "xs1.h" 3
void outuint(chanend c, unsigned val);
# 956 "xs1.h" 3
unsigned char inuchar(chanend c);
# 972 "xs1.h" 3
unsigned inuint(chanend c);
# 989 "xs1.h" 3
void inuchar_byref(chanend c, unsigned char &val);
# 1007 "xs1.h" 3
void inuint_byref(chanend c, unsigned &val);
# 1017 "xs1.h" 3
void sync(void port p);
# 1028 "xs1.h" 3
unsigned peek(void port p);
# 1042 "xs1.h" 3
void clearbuf(void port p);
# 1058 "xs1.h" 3
unsigned endin( void port p);
# 1075 "xs1.h" 3
unsigned partin( void port p, unsigned n);
# 1091 "xs1.h" 3
void partout( void port p, unsigned n, unsigned val);
# 1109 "xs1.h" 3
unsigned partout_timed( void port p, unsigned n, unsigned val, unsigned t);
# 1127 "xs1.h" 3
{unsigned , unsigned } partin_timestamped( void port p, unsigned n);
# 1145 "xs1.h" 3
unsigned partout_timestamped( void port p, unsigned n, unsigned val);
# 1159 "xs1.h" 3
void outct(chanend c, unsigned char val);
# 1174 "xs1.h" 3
void chkct(chanend c, unsigned char val);
# 1189 "xs1.h" 3
unsigned char inct(chanend c);
# 1204 "xs1.h" 3
void inct_byref(chanend c, unsigned char &val);
# 1218 "xs1.h" 3
int testct(chanend c);
# 1231 "xs1.h" 3
int testwct(chanend c);
# 1246 "xs1.h" 3
void soutct(streaming chanend c, unsigned char val);
# 1262 "xs1.h" 3
void schkct(streaming chanend c, unsigned char val);
# 1278 "xs1.h" 3
unsigned char sinct(streaming chanend c);
# 1294 "xs1.h" 3
void sinct_byref(streaming chanend c, unsigned char &val);
# 1308 "xs1.h" 3
int stestct(streaming chanend c);
# 1322 "xs1.h" 3
int stestwct(streaming chanend c);
# 1337 "xs1.h" 3
transaction out_char_array(chanend c, const char src[], unsigned size);
# 1350 "xs1.h" 3
transaction in_char_array(chanend c, char src[], unsigned size);
# 1373 "xs1.h" 3
void crc32(unsigned &checksum, unsigned data, unsigned poly);
# 1397 "xs1.h" 3
unsigned crc8shr(unsigned &checksum, unsigned data, unsigned poly);
# 1412 "xs1.h" 3
{unsigned, unsigned} lmul(unsigned a, unsigned b, unsigned c, unsigned d);
# 1426 "xs1.h" 3
{unsigned, unsigned} mac(unsigned a, unsigned b, unsigned c, unsigned d);
# 1440 "xs1.h" 3
{signed, unsigned} macs(signed a, signed b, signed c, unsigned d);
# 1454 "xs1.h" 3
signed sext(unsigned a, unsigned b);
# 1468 "xs1.h" 3
unsigned zext(unsigned a, unsigned b);
# 1481 "xs1.h" 3
void pinseq(unsigned val);
# 1494 "xs1.h" 3
void pinsneq(unsigned val);
# 1509 "xs1.h" 3
void pinseq_at(unsigned val, unsigned time);
# 1524 "xs1.h" 3
void pinsneq_at(unsigned val, unsigned time);
# 1537 "xs1.h" 3
void timerafter(unsigned val);
# 1573 "xs1.h" 3
unsigned getps(unsigned reg);
# 1584 "xs1.h" 3
void setps(unsigned reg, unsigned value);
# 1606 "xs1.h" 3
int read_pswitch_reg(unsigned coreid, unsigned reg, unsigned &data);
# 1630 "xs1.h" 3
int read_sswitch_reg(unsigned coreid, unsigned reg, unsigned &data);
# 1652 "xs1.h" 3
int write_pswitch_reg(unsigned coreid, unsigned reg, unsigned data);
# 1672 "xs1.h" 3
int write_pswitch_reg_no_ack(unsigned coreid, unsigned reg, unsigned data);
# 1691 "xs1.h" 3
int write_sswitch_reg(unsigned coreid, unsigned reg, unsigned data);
# 1712 "xs1.h" 3
int write_sswitch_reg_no_ack(unsigned coreid, unsigned reg, unsigned data);
# 1728 "xs1.h" 3
int read_node_config_reg(core c, unsigned reg, unsigned &data);
# 1743 "xs1.h" 3
int write_node_config_reg(core c, unsigned reg, unsigned data);
# 1759 "xs1.h" 3
int write_node_config_reg_no_ack(core c, unsigned reg, unsigned data);
# 1778 "xs1.h" 3
int read_periph_8(core c, unsigned peripheral, unsigned base_address,
                  unsigned size, unsigned char data[]);
# 1797 "xs1.h" 3
int write_periph_8(core c, unsigned peripheral, unsigned base_address,
                    unsigned size, const unsigned char data[]);
# 1818 "xs1.h" 3
int write_periph_8_no_ack(core c, unsigned peripheral,
                           unsigned base_address, unsigned size,
                           const unsigned char data[]);
# 1840 "xs1.h" 3
int read_periph_32(core c, unsigned peripheral, unsigned base_address,
                   unsigned size, unsigned data[]);
# 1861 "xs1.h" 3
int write_periph_32(core c, unsigned peripheral, unsigned base_address,
                   unsigned size, const unsigned data[]);
# 1884 "xs1.h" 3
int write_periph_32_no_ack(core c, unsigned peripheral,
                           unsigned base_address, unsigned size,
                           const unsigned data[]);
# 1895 "xs1.h" 3
unsigned get_core_id(void);
# 1903 "xs1.h" 3
unsigned get_thread_id(void);
# 1908 "xs1.h" 3
extern int __builtin_getid(void);
# 5 "/home/joseph/School/comp/joslewis/HW02-HotPotato/.build_Debug/XK-1A.h" 2
# 13 "/home/joseph/School/comp/joslewis/HW02-HotPotato/.build_Debug/XK-1A.h"
extern core stdcore[1];
# 22 "platform.h" 2 3
# 4 "../src/HW02-HotPotato.xc" 2










void worker ( unsigned int workerid, chanend left , chanend right ) ;
int worker_fx(chanend tosend, int packet, timer t, char dir[], unsigned int worker);
void buttonlistenertask (chanend left, chanend right);
void btn_sim();


in port iButton1 =  on stdcore[0]: 0x10900 ;
out port oButtonDriver1 =  0x10200 ;

int main()
{
	chan a;
	chan b;
	chan c;
	chan d;

	par
	{
			buttonlistenertask(c, d);
			worker(1, d, a);
			worker(2, a, b);
			worker(3, b, c);

			btn_sim();
	}
}


void worker( unsigned int workerid, chanend left, chanend right)
{
	timer t;
	int packet;
	unsigned int currtime;


	if(workerid == 1)
		right <: 1;



	while(1)
	{
		t :> currtime;
		currtime +=  ( (( 100U ) * 1000000U) /1000) ;

		select
		{
				case left :> packet:
					if(worker_fx(right, packet, t, "left", workerid))
						return;
				break;
				case right :> packet:
					if(worker_fx(left, packet, t, "right", workerid))
						return;
				break;
				case t when  __builtin_timer_after(currtime)  :> void:
					return;
				break;
		}
	}
}


int worker_fx(chanend tosend, int packet, timer t, char dir[], unsigned int worker)
{
	char msg[64];
	unsigned int currtime;


	sprintf(msg, "Packet recieved on %i from %s, hop is: %i\n",worker, dir, packet);
	printstr(msg);


	packet++;




	t :> currtime;
	currtime +=  ( (( 100U ) * 1000000U) /1000000)  *  10 ;
	t when  __builtin_timer_after(currtime)  :> void;


	if(packet <= 10)
		tosend <: packet;


	return (packet >  10 );
}
# 118 "../src/HW02-HotPotato.xc"
void buttonlistenertask (chanend left, chanend right)
{
	timer t;
	unsigned int currtime;
	unsigned int reverse_next;
	int packet;
	reverse_next = 0;


	iButton1 when  __builtin_pins_eq(1)  :> void;


	while(1)
	{


		t :> currtime;
		currtime +=  ( (( 100U ) * 1000000U) /1000)  *  2 ;


		select
		{
			case left :> packet:
				if(reverse_next)
				{
					left <: packet;
					reverse_next = 0;
				}
				else
					right <: packet;
			break;
			case right :> packet:
				if(reverse_next)
				{
					right <: packet;
					reverse_next = 0;
				}
				else
					left <: packet;
			break;

			case iButton1 when  __builtin_pins_eq(0)  :> void:
				if(!reverse_next)
					reverse_next = 2;
			break;

			case t when  __builtin_timer_after(currtime)  :> void:
				return;
			break;
		}
	}
}
# 179 "../src/HW02-HotPotato.xc"
void btn_sim()
{
	timer t;
	unsigned int currtime;


	oButtonDriver1 <: 1;



	t :> currtime;
	currtime +=  ( (( 100U ) * 1000000U) /1000000)  *  1 ;
	t when  __builtin_timer_after(currtime)  :> void;


	oButtonDriver1 <: 0;


	t :> currtime;
	currtime +=  ( (( 100U ) * 1000000U) /1000000)  *  1 ;
	t when  __builtin_timer_after(currtime)  :> void;


	oButtonDriver1 <: 1;


}
