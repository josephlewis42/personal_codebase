          .file     "../src/HW02-HotPotato.xc"
          .section .netinfo,       "", @netinfo
.globl iButton1.info, "i:p"
iButton1.info:
          .int      0x00010900
          .long stdcore
          .section .dp.data,       "adw", @progbits
.globl oButtonDriver1, "o:p"
.type  oButtonDriver1, @object
.size oButtonDriver1, 4
.cc_top oButtonDriver1.data, oButtonDriver1
          .align    4
oButtonDriver1:
          .int      0x00010200
.cc_bottom oButtonDriver1.data
          .align    4
          .section .globcode,      "ax",  @progbits
          .align    2
.cc_top oButtonDriver1.globcode.init, oButtonDriver1
.LC0:
          ldw       r0, dp[oButtonDriver1] 
          setc      res[r0], 0x8
          ldc       r1, _default_clkblk
          setclk    res[r0], r1
          retsp     0x0 
.cc_bottom oButtonDriver1.globcode.init
          .section .ctors,         "aw",  @progbits
          .align    4
          .int      .LC0
          .section .globcode,      "ax",  @progbits
.cc_top oButtonDriver1.globcode.fini, oButtonDriver1
.LC1:
          ldw       r0, dp[oButtonDriver1] 
          setc      res[r0], 0x0
          retsp     0x0 
.cc_bottom oButtonDriver1.globcode.fini
          .section .dtors,         "aw",  @progbits
          .align    4
          .int      .LC1
.extern printf, "f{si}(&(a(:c:uc)),va)"
.extern scanf, "f{si}(&(a(:c:uc)),va)"
.extern sscanf, "f{si}(&(a(:c:uc)),&(a(:c:uc)),va)"
.extern getchar, "f{si}(0)"
.extern putchar, "f{si}(si)"
.extern puts, "f{si}(&(a(:c:uc)))"
.extern perror, "f{0}(&(a(:c:uc)))"
.extern sprintf, "f{si}(&(a(:uc)),&(a(:c:uc)),va)"
.extern remove, "f{si}(&(a(:c:uc)))"
.extern rename, "f{si}(&(a(:c:uc)),&(a(:c:uc)))"
.extern diprintf, "f{si}(si,&(a(:c:uc)),va)"
.extern fcloseall, "f{si}(0)"
.extern iprintf, "f{si}(&(a(:c:uc)),va)"
.extern iscanf, "f{si}(&(a(:c:uc)),va)"
.extern siprintf, "f{si}(&(a(:uc)),&(a(:c:uc)),va)"
.extern siscanf, "f{si}(&(a(:c:uc)),&(a(:c:uc)),va)"
.extern snprintf, "f{si}(&(a(:uc)),ui,&(a(:c:uc)),va)"
.extern sniprintf, "f{si}(&(a(:uc)),ui,&(a(:c:uc)),va)"
.extern printchar, "f{si}(uc)"
.extern printcharln, "f{si}(uc)"
.extern printint, "f{si}(si)"
.extern printintln, "f{si}(si)"
.extern printuint, "f{si}(ui)"
.extern printuintln, "f{si}(ui)"
.extern printhex, "f{si}(ui)"
.extern printhexln, "f{si}(ui)"
.extern printstr, "f{si}(&(a(:c:uc)))"
.extern printstrln, "f{si}(&(a(:c:uc)))"
.extern configure_in_port_handshake, "f{0}(w:p,i:p,o:p,ck)"
.extern configure_out_port_handshake, "f{0}(w:p,i:p,o:p,ck,ui)"
.extern configure_in_port_strobed_master, "f{0}(w:p,o:p,:ck)"
.extern configure_out_port_strobed_master, "f{0}(w:p,o:p,:ck,ui)"
.extern configure_in_port_strobed_slave, "f{0}(w:p,i:p,ck)"
.extern configure_out_port_strobed_slave, "f{0}(w:p,i:p,ck,ui)"
.extern configure_in_port, "f{0}(w:p,:ck)"
.extern configure_in_port_no_ready, "f{0}(w:p,:ck)"
.extern configure_out_port, "f{0}(w:p,:ck,ui)"
.extern configure_out_port_no_ready, "f{0}(w:p,:ck,ui)"
.extern configure_port_clock_output, "f{0}(w:p,:ck)"
.extern start_port, "f{0}(w:p)"
.extern stop_port, "f{0}(w:p)"
.extern configure_clock_src, "f{0}(ck,w:p)"
.extern configure_clock_ref, "f{0}(ck,uc)"
.extern configure_clock_rate, "f{0}(ck,ui,ui)"
.extern configure_clock_rate_at_least, "f{0}(ck,ui,ui)"
.extern configure_clock_rate_at_most, "f{0}(ck,ui,ui)"
.extern set_clock_src, "f{0}(ck,w:p)"
.extern set_clock_ref, "f{0}(ck)"
.extern set_clock_div, "f{0}(ck,uc)"
.extern set_clock_rise_delay, "f{0}(ck,ui)"
.extern set_clock_fall_delay, "f{0}(ck,ui)"
.extern set_port_clock, "f{0}(w:p,:ck)"
.extern set_port_ready_src, "f{0}(w:p,w:p)"
.extern set_clock_ready_src, "f{0}(ck,w:p)"
.extern set_clock_on, "f{0}(ck)"
.extern set_clock_off, "f{0}(ck)"
.extern start_clock, "f{0}(ck)"
.extern stop_clock, "f{0}(ck)"
.extern set_port_use_on, "f{0}(w:p)"
.extern set_port_use_off, "f{0}(w:p)"
.extern set_port_mode_data, "f{0}(w:p)"
.extern set_port_mode_clock, "f{0}(w:p)"
.extern set_port_mode_ready, "f{0}(w:p)"
.extern set_port_drive, "f{0}(w:p)"
.extern set_port_drive_low, "f{0}(w:p)"
.extern set_port_pull_up, "f{0}(w:p)"
.extern set_port_pull_down, "f{0}(w:p)"
.extern set_port_pull_none, "f{0}(w:p)"
.extern set_port_master, "f{0}(w:p)"
.extern set_port_slave, "f{0}(w:p)"
.extern set_port_no_ready, "f{0}(w:p)"
.extern set_port_strobed, "f{0}(w:p)"
.extern set_port_handshake, "f{0}(w:p)"
.extern set_port_no_sample_delay, "f{0}(w:p)"
.extern set_port_sample_delay, "f{0}(w:p)"
.extern set_port_no_inv, "f{0}(w:p)"
.extern set_port_inv, "f{0}(w:p)"
.extern set_port_shift_count, "f{0}(w:p,ui)"
.extern set_pad_delay, "f{0}(w:p,ui)"
.extern set_thread_fast_mode_on, "f{0}(0)"
.extern set_thread_fast_mode_off, "f{0}(0)"
.extern start_streaming_slave, "f{0}(chd)"
.extern start_streaming_master, "f{0}(chd)"
.extern stop_streaming_slave, "f{0}(chd)"
.extern stop_streaming_master, "f{0}(chd)"
.extern outuchar, "f{0}(chd,uc)"
.extern outuint, "f{0}(chd,ui)"
.extern inuchar, "f{uc}(chd)"
.extern inuint, "f{ui}(chd)"
.extern inuchar_byref, "f{0}(chd,&(uc))"
.extern inuint_byref, "f{0}(chd,&(ui))"
.extern sync, "f{0}(w:p)"
.extern peek, "f{ui}(w:p)"
.extern clearbuf, "f{0}(w:p)"
.extern endin, "f{ui}(w:p)"
.extern partin, "f{ui}(w:p,ui)"
.extern partout, "f{0}(w:p,ui,ui)"
.extern partout_timed, "f{ui}(w:p,ui,ui,ui)"
.extern partin_timestamped, "f{ui,ui}(w:p,ui)"
.extern partout_timestamped, "f{ui}(w:p,ui,ui)"
.extern outct, "f{0}(chd,uc)"
.extern chkct, "f{0}(chd,uc)"
.extern inct, "f{uc}(chd)"
.extern inct_byref, "f{0}(chd,&(uc))"
.extern testct, "f{si}(chd)"
.extern testwct, "f{si}(chd)"
.extern soutct, "f{0}(m:chd,uc)"
.extern schkct, "f{0}(m:chd,uc)"
.extern sinct, "f{uc}(m:chd)"
.extern sinct_byref, "f{0}(m:chd,&(uc))"
.extern stestct, "f{si}(m:chd)"
.extern stestwct, "f{si}(m:chd)"
.extern out_char_array, "ft{0}(chd,&(a(:c:uc)),ui)"
.extern in_char_array, "ft{0}(chd,&(a(:uc)),ui)"
.extern crc32, "f{0}(&(ui),ui,ui)"
.extern crc8shr, "f{ui}(&(ui),ui,ui)"
.extern lmul, "f{ui,ui}(ui,ui,ui,ui)"
.extern mac, "f{ui,ui}(ui,ui,ui,ui)"
.extern macs, "f{si,ui}(si,si,si,ui)"
.extern sext, "f{si}(ui,ui)"
.extern zext, "f{ui}(ui,ui)"
.extern pinseq, "f{0}(ui)"
.extern pinsneq, "f{0}(ui)"
.extern pinseq_at, "f{0}(ui,ui)"
.extern pinsneq_at, "f{0}(ui,ui)"
.extern timerafter, "f{0}(ui)"
.extern getps, "f{ui}(ui)"
.extern setps, "f{0}(ui,ui)"
.extern read_pswitch_reg, "f{si}(ui,ui,&(ui))"
.extern read_sswitch_reg, "f{si}(ui,ui,&(ui))"
.extern write_pswitch_reg, "f{si}(ui,ui,ui)"
.extern write_pswitch_reg_no_ack, "f{si}(ui,ui,ui)"
.extern write_sswitch_reg, "f{si}(ui,ui,ui)"
.extern write_sswitch_reg_no_ack, "f{si}(ui,ui,ui)"
.extern read_node_config_reg, "f{si}(cr,ui,&(ui))"
.extern write_node_config_reg, "f{si}(cr,ui,ui)"
.extern write_node_config_reg_no_ack, "f{si}(cr,ui,ui)"
.extern read_periph_8, "f{si}(cr,ui,ui,ui,&(a(:uc)))"
.extern write_periph_8, "f{si}(cr,ui,ui,ui,&(a(:c:uc)))"
.extern write_periph_8_no_ack, "f{si}(cr,ui,ui,ui,&(a(:c:uc)))"
.extern read_periph_32, "f{si}(cr,ui,ui,ui,&(a(:ui)))"
.extern write_periph_32, "f{si}(cr,ui,ui,ui,&(a(:c:ui)))"
.extern write_periph_32_no_ack, "f{si}(cr,ui,ui,ui,&(a(:c:ui)))"
.extern get_core_id, "f{ui}(0)"
.extern get_thread_id, "f{ui}(0)"
.extern __builtin_getid, "f{si}(0)"
.extern worker, "f{0}(ui,chd,chd)"
.extern worker_fx, "f{si}(chd,si,t,&(a(:uc)),ui)"
.extern buttonlistenertask, "f{0}(chd,chd)"
.extern btn_sim, "f{0}(0)"
          .text
          .align    2
.cc_top main.function,main
          .align    4
.call main, thread.anon.0
.call main, thread.anon.1
.call thread.anon.1, buttonlistenertask
.call main, thread.anon.2
.call thread.anon.2, worker
.call main, thread.anon.4
.call thread.anon.4, worker
.call main, thread.anon.6
.call thread.anon.6, worker
.call main, thread.anon.9
.call thread.anon.9, btn_sim
.linkset .LLNK7, buttonlistenertask.nstackwords + 1
.linkset .LLNK6, .LLNK7 + btn_sim.nstackwords
.linkset .LLNK5, .LLNK6 $M .LLNK6
.linkset .LLNK4, .LLNK5 + 1
.linkset .LLNK3, .LLNK4 + worker.nstackwords
.linkset .LLNK2, .LLNK3 $M .LLNK3
.linkset .LLNK1, .LLNK2 + 1
.linkset .LLNK0, .LLNK1 + 9
.linkset .LLNK11, .LLNK1 + worker.nstackwords
.linkset .LLNK10, .LLNK11 $M .LLNK11
.linkset .LLNK9, .LLNK10 + 1
.linkset .LLNK8, .LLNK9 + 8
.globl main, "f{si}(0)"
.globl main.nstackwords
.globl main.maxthreads
.globl main.maxtimers
.globl main.maxchanends
.globl main.maxsync
.type  main, @function
.linkset main.locnoside, 1
.linkset main.locnochandec, 0
.linkset .LLNK16, .LLNK9 + worker.nstackwords
.linkset .LLNK15, .LLNK16 $M .LLNK16
.linkset .LLNK14, buttonlistenertask.nstackwords $M .LLNK15
.linkset .LLNK13, buttonlistenertask.nstackwords $M .LLNK14
.linkset .LLNK12, .LLNK13 + 12
.linkset main.nstackwords, .LLNK12
main:
          entsp     0xc 
          stw       r4, sp[0x1] 
          stw       r5, sp[0x2] 
          stw       r6, sp[0x3] 
          stw       r7, sp[0x4] 
          stw       r8, sp[0x5] 
          stw       r9, sp[0x6] 
          stw       r10, sp[0x7] 
          getr      r1, 0x2
          getr      r0, 0x2
          setd      res[r1], r0
          setd      res[r0], r1
          stw       r1, sp[0x8] 
          stw       r0, sp[0x9] 
          getr      r10, 0x2
          getr      r9, 0x2
          setd      res[r10], r9
          setd      res[r9], r10
          getr      r4, 0x2
          getr      r8, 0x2
          setd      res[r4], r8
          setd      res[r8], r4
          getr      r5, 0x2
          getr      r7, 0x2
          setd      res[r5], r7
          setd      res[r7], r5
          getr      r6, 0x3
          getst     r0, res[r6]
          ldap      r11, .L3
          ldaw      r11, sp[0x0] 
          init      t[r0]:sp, r11
          ldap      r11, .L3
          init      t[r0]:pc, r11
          set       t[r0]:r5, r7
          getst     r0, res[r6]
          ldap      r11, .L6
          ldaw      r11, sp[0x0] 
          init      t[r0]:sp, r11
          ldap      r11, .L6
          init      t[r0]:pc, r11
          set       t[r0]:r5, r10
          getst     r0, res[r6]
          ldap      r11, .L9
          ldaw      r11, sp[0x0] 
          init      t[r0]:sp, r11
          ldap      r11, .L9
          init      t[r0]:pc, r11
          set       t[r0]:r4, r9
          set       t[r0]:r5, r8
          getst     r0, res[r6]
          ldap      r11, .L12
          ldaw      r11, sp[0x0] 
          init      t[r0]:sp, r11
          ldap      r11, .L12
          init      t[r0]:pc, r11
          msync     res[r6]
.L15:
.L1:
          mov       r0, r4
          mov       r1, r5
.L17:
          bl        buttonlistenertask 
.L0:
          msync     res[r6]
          mjoin     res[r6]
.L2:
          freer     res[r6]
          ldw       r0, sp[0x8] 
          freer     res[r0]
          ldw       r0, sp[0x9] 
          freer     res[r0]
          freer     res[r10]
          freer     res[r9]
          freer     res[r4]
          freer     res[r8]
          freer     res[r5]
          freer     res[r7]
          ldw       r4, sp[0x1] 
          ldw       r5, sp[0x2] 
          ldw       r6, sp[0x3] 
          ldw       r7, sp[0x4] 
          ldw       r8, sp[0x5] 
          ldw       r9, sp[0x6] 
          ldw       r10, sp[0x7] 
.L16:
          retsp     0xc 
.xtathreadstart
          .file     1 "../src/HW02-HotPotato.xc"
          .loc      1 37 0

.L12:
.linkset .LLNK19, buttonlistenertask.nstackwords - buttonlistenertask.nstackwords
.linkset .LLNK18, .LLNK19 + buttonlistenertask.nstackwords
.linkset .LLNK17, .LLNK18 + 1
          extsp     .LLNK17 
.L14:
.L18:
          bl        btn_sim 
.L13:
          ssync     
.xtathreadstop
          ssync     
.xtathreadstart
          .loc      1 35 0

.L9:
.linkset .LLNK22, .LLNK5 - buttonlistenertask.nstackwords
.linkset .LLNK21, .LLNK22 + buttonlistenertask.nstackwords
.linkset .LLNK20, .LLNK21 + 1
          extsp     .LLNK20 
.L11:
          mkmsk     r0, 0x2
          mov       r1, r4
          mov       r2, r5
.L19:
          bl        worker 
.L10:
          ssync     
.xtathreadstop
          ssync     
.xtathreadstart
          .loc      1 34 0

.L6:
.linkset .LLNK25, .LLNK2 - buttonlistenertask.nstackwords
.linkset .LLNK24, .LLNK25 + buttonlistenertask.nstackwords
.linkset .LLNK23, .LLNK24 + 1
          extsp     .LLNK23 
          ldw       r4, sp[.LLNK0] 
.L8:
          ldc       r0, 0x2
          mov       r1, r4
          mov       r2, r5
.L20:
          bl        worker 
.L7:
          ssync     
.xtathreadstop
          ssync     
.xtathreadstart
          .loc      1 33 0

.L3:
.linkset .LLNK28, .LLNK10 - buttonlistenertask.nstackwords
.linkset .LLNK27, .LLNK28 + buttonlistenertask.nstackwords
.linkset .LLNK26, .LLNK27 + 1
          extsp     .LLNK26 
          ldw       r10, sp[.LLNK8] 
.L5:
          mkmsk     r0, 0x1
          mov       r1, r5
          mov       r2, r10
.L21:
          bl        worker 
.L4:
          ssync     
.xtathreadstop
          ssync     
.size main, .-main
.cc_bottom main.function
.linkset .LLNK34, buttonlistenertask.maxchanends + btn_sim.maxchanends
.linkset .LLNK33, .LLNK34 + worker.maxchanends
.linkset .LLNK32, .LLNK33 + worker.maxchanends
.linkset .LLNK31, .LLNK32 + worker.maxchanends
.linkset .LLNK30, 8 + .LLNK31
.linkset .LLNK29, 8 $M .LLNK30
.linkset main.maxchanends, .LLNK29
.linkset .LLNK38, buttonlistenertask.maxtimers + btn_sim.maxtimers
.linkset .LLNK37, .LLNK38 + worker.maxtimers
.linkset .LLNK36, .LLNK37 + worker.maxtimers
.linkset .LLNK35, .LLNK36 + worker.maxtimers
.linkset main.maxtimers, .LLNK35
.linkset .LLNK46, buttonlistenertask.maxthreads - 1
.linkset .LLNK45, 1 + .LLNK46
.linkset .LLNK44, 1 $M .LLNK45
.linkset .LLNK49, btn_sim.maxthreads - 1
.linkset .LLNK48, 1 + .LLNK49
.linkset .LLNK47, 1 $M .LLNK48
.linkset .LLNK43, .LLNK44 + .LLNK47
.linkset .LLNK52, worker.maxthreads - 1
.linkset .LLNK51, 1 + .LLNK52
.linkset .LLNK50, 1 $M .LLNK51
.linkset .LLNK42, .LLNK43 + .LLNK50
.linkset .LLNK55, worker.maxthreads - 1
.linkset .LLNK54, 1 + .LLNK55
.linkset .LLNK53, 1 $M .LLNK54
.linkset .LLNK41, .LLNK42 + .LLNK53
.linkset .LLNK58, worker.maxthreads - 1
.linkset .LLNK57, 1 + .LLNK58
.linkset .LLNK56, 1 $M .LLNK57
.linkset .LLNK40, .LLNK41 + .LLNK56
.linkset .LLNK39, 1 $M .LLNK40
.linkset main.maxthreads, .LLNK39
.cc_top worker.function,worker
          .align    4
.call worker, worker_fx
          .section .cp.string,     "ac", @progbits
.cc_top .LC2.string, .LC2
          .align    4
.LC2:
          .ascii    "left\0"
.cc_bottom .LC2.string
.call worker, worker_fx
.cc_top .LC3.string, .LC3
          .align    4
.LC3:
          .ascii    "right\0"
.cc_bottom .LC3.string
.call worker, __builtin_timer_after
.set __builtin_timer_after, 0
.linkset __builtin_timer_after.locnoside, 0
.linkset __builtin_timer_after.locnochandec, 1
          .text
.globl worker, "f{0}(ui,chd,chd)"
.globl worker.nstackwords
.globl worker.maxthreads
.globl worker.maxtimers
.globl worker.maxchanends
.globl worker.maxsync
.type  worker, @function
.linkset worker.locnoside, 0
.linkset worker.locnochandec, 1
.linkset .LLNK61, worker_fx.nstackwords $M worker_fx.nstackwords
.linkset .LLNK60, .LLNK61 $M .LLNK61
.linkset .LLNK59, .LLNK60 + 9
.linkset worker.nstackwords, .LLNK59
worker:
          entsp     0x9 
          stw       r0, sp[0x3] 
          stw       r1, sp[0x4] 
          stw       r2, sp[0x5] 
          getr      r0, 0x1
          stw       r0, sp[0x6] 
.L22:
.L27:
          ldw       r0, sp[0x3] 
          eq        r0, r0, 0x1
          bt        r0, .L24 
          bu        .L23 
.L24:
.L26:
          ldw       r0, sp[0x5] 
          outct     res[r0], 0x1 
          ldw       r0, sp[0x5] 
          chkct     res[r0], 0x1 
          ldw       r1, sp[0x5] 
          mkmsk     r0, 0x1
.L77:
          out       res[r1], r0 
          ldw       r0, sp[0x5] 
          outct     res[r0], 0x1 
          ldw       r0, sp[0x5] 
          chkct     res[r0], 0x1 
.L23:
.L29:
.L71:
          mkmsk     r0, 0x1
          bt        r0, .L30 
          bu        .L28 
.L30:
.L32:
.L33:
          ldw       r0, sp[0x6] 
          setc      res[r0], 0x1
          ldw       r0, sp[0x6] 
.L78:
          in        r0, res[r0] 
          stw       r0, sp[0x8] 
          ldw       r0, sp[0x8] 
          stw       r0, sp[0x8] 
.L34:
.L35:
          ldw       r1, sp[0x8] 
          ldw       r0, cp[.LC4]
          .section .cp.const4,     "acM", @progbits, 4
.cc_top .LC4.data, .LC4
          .align    4
.LC4:
          .int      0x000186a0

.cc_bottom .LC4.data
          .text
          add       r0, r1, r0
          stw       r0, sp[0x8] 
          clre      
          ldw       r0, sp[0x4] 
          ldap      r11, .L39
          setv      res[r0], r11
          ldw       r0, sp[0x4] 
          eeu       res[r0]
          ldw       r0, sp[0x5] 
          ldap      r11, .L51
          setv      res[r0], r11
          ldw       r0, sp[0x5] 
          eeu       res[r0]
          ldw       r1, sp[0x8] 
          ldw       r0, sp[0x6] 
          setd      res[r0], r1
          ldw       r0, sp[0x6] 
          setc      res[r0], 0x9
.L66:
          ldw       r0, sp[0x6] 
          ldap      r11, .L63
          setv      res[r0], r11
          ldw       r0, sp[0x6] 
          eeu       res[r0]
.xtabranch .L63,.L51,.L39
          waiteu    
.L39:
          ldw       r0, sp[0x4] 
          chkct     res[r0], 0x1 
          ldw       r0, sp[0x4] 
          outct     res[r0], 0x1 
          ldw       r0, sp[0x4] 
.L79:
          in        r0, res[r0] 
          stw       r0, sp[0x7] 
          ldw       r0, sp[0x7] 
          stw       r0, sp[0x7] 
          ldw       r0, sp[0x4] 
          chkct     res[r0], 0x1 
          ldw       r0, sp[0x4] 
          outct     res[r0], 0x1 
.L42:
.L49:
          ldw       r1, sp[0x7] 
          ldaw      r11, cp[.LC2] 
          mov       r3, r11
          ldw       r11, sp[0x3] 
          ldw       r0, sp[0x5] 
          ldw       r2, sp[0x6] 
          stw       r11, sp[0x1] 
          ldc       r11, 0x5
          stw       r11, sp[0x2] 
.L80:
          bl        worker_fx 
.L46:
          bt        r0, .L44 
          bu        .L43 
.L44:
.L47:
          ldw       r0, sp[0x6] 
          freer     res[r0]
.L73:
          retsp     0x9 
.L43:
          bu        .L38 
.L51:
          ldw       r0, sp[0x5] 
          chkct     res[r0], 0x1 
          ldw       r0, sp[0x5] 
          outct     res[r0], 0x1 
          ldw       r0, sp[0x5] 
.L81:
          in        r0, res[r0] 
          stw       r0, sp[0x7] 
          ldw       r0, sp[0x7] 
          stw       r0, sp[0x7] 
          ldw       r0, sp[0x5] 
          chkct     res[r0], 0x1 
          ldw       r0, sp[0x5] 
          outct     res[r0], 0x1 
.L54:
.L61:
          ldw       r1, sp[0x7] 
          ldaw      r11, cp[.LC3] 
          mov       r3, r11
          ldw       r11, sp[0x3] 
          ldw       r0, sp[0x4] 
          ldw       r2, sp[0x6] 
          stw       r11, sp[0x1] 
          ldc       r11, 0x6
          stw       r11, sp[0x2] 
.L82:
          bl        worker_fx 
.L58:
          bt        r0, .L56 
          bu        .L55 
.L56:
.L59:
          ldw       r0, sp[0x6] 
          freer     res[r0]
.L74:
          retsp     0x9 
.L55:
          bu        .L38 
.L63:
          ldw       r0, sp[0x6] 
.L83:
          in        r0, res[r0] 
.L67:
.L68:
          ldw       r0, sp[0x6] 
          freer     res[r0]
.L75:
          retsp     0x9 
          bu        .L38 
.L36:
.L38:
          bu        .L29 
.L28:
          ldw       r0, sp[0x6] 
          freer     res[r0]
.L76:
          retsp     0x9 
.size worker, .-worker
.cc_bottom worker.function
.linkset .LLNK62, worker_fx.maxchanends $M worker_fx.maxchanends
.linkset worker.maxchanends, .LLNK62
.linkset .LLNK65, 1 + worker_fx.maxtimers
.linkset .LLNK64, 1 $M .LLNK65
.linkset .LLNK66, 1 + worker_fx.maxtimers
.linkset .LLNK63, .LLNK64 $M .LLNK66
.linkset worker.maxtimers, .LLNK63
.linkset .LLNK70, worker_fx.maxthreads - 1
.linkset .LLNK69, 1 + .LLNK70
.linkset .LLNK68, 1 $M .LLNK69
.linkset .LLNK72, worker_fx.maxthreads - 1
.linkset .LLNK71, 1 + .LLNK72
.linkset .LLNK67, .LLNK68 $M .LLNK71
.linkset worker.maxthreads, .LLNK67
.cc_top worker_fx.function,worker_fx
          .align    4
.call worker_fx, sprintf
          .section .cp.string,     "ac", @progbits
.cc_top .LC5.string, .LC5
          .align    4
.LC5:
          .ascii    "Packet recieved on %i from %s, hop is: %i\n\0"
.cc_bottom .LC5.string
.call worker_fx, printstr
.call worker_fx, __builtin_timer_after
          .text
.globl worker_fx, "f{si}(chd,si,t,&(a(:uc)),ui)"
.globl worker_fx.nstackwords
.globl worker_fx.maxthreads
.globl worker_fx.maxtimers
.globl worker_fx.maxchanends
.globl worker_fx.maxsync
.type  worker_fx, @function
.linkset worker_fx.locnoside, 0
.linkset worker_fx.locnochandec, 1
.linkset .LLNK75, sprintf.nstackwords $M printstr.nstackwords
.linkset .LLNK74, .LLNK75 $M .LLNK75
.linkset .LLNK73, .LLNK74 + 23
.linkset worker_fx.nstackwords, .LLNK73
worker_fx:
          entsp     0x17 
          stw       r0, sp[0x2] 
          stw       r1, sp[0x3] 
          stw       r2, sp[0x4] 
          stw       r3, sp[0x5] 
.L84:
.L86:
          ldaw      r0, sp[0x6] 
          ldaw      r11, cp[.LC5] 
          mov       r1, r11
          ldw       r2, sp[0x18] 
          ldw       r3, sp[0x5] 
          add       r3, r3, 0x0
          ldw       r11, sp[0x3] 
          stw       r11, sp[0x1] 
.L108:
          bl        sprintf 
.L85:
.L87:
.L89:
          ldaw      r0, sp[0x6] 
          ldc       r1, 0x40
.L109:
          bl        printstr 
.L88:
.L90:
.L91:
          ldw       r0, sp[0x3] 
          add       r0, r0, 0x1
          stw       r0, sp[0x3] 
.L92:
.L93:
          ldw       r0, sp[0x4] 
          setc      res[r0], 0x1
          ldw       r0, sp[0x4] 
.L110:
          in        r0, res[r0] 
          stw       r0, sp[0x16] 
          ldw       r0, sp[0x16] 
          stw       r0, sp[0x16] 
.L94:
.L95:
          ldw       r1, sp[0x16] 
          ldc       r0, 0x3e8
          add       r0, r1, r0
          stw       r0, sp[0x16] 
.L96:
.L98:
          ldw       r1, sp[0x16] 
          ldw       r0, sp[0x4] 
          setd      res[r0], r1
          ldw       r0, sp[0x4] 
          setc      res[r0], 0x9
.L97:
          ldw       r0, sp[0x4] 
.L111:
          in        r0, res[r0] 
.L99:
.L104:
          ldw       r1, sp[0x3] 
          ldc       r0, 0xa
          lss       r0, r0, r1
          bf        r0, .L101 
          bu        .L100 
.L101:
.L103:
          ldw       r0, sp[0x2] 
          outct     res[r0], 0x1 
          ldw       r0, sp[0x2] 
          chkct     res[r0], 0x1 
          ldw       r1, sp[0x2] 
          ldw       r0, sp[0x3] 
.L112:
          out       res[r1], r0 
          ldw       r0, sp[0x2] 
          outct     res[r0], 0x1 
          ldw       r0, sp[0x2] 
          chkct     res[r0], 0x1 
.L100:
.L105:
          ldw       r1, sp[0x3] 
          ldc       r0, 0xa
          lss       r0, r0, r1
.L107:
          retsp     0x17 
.size worker_fx, .-worker_fx
.cc_bottom worker_fx.function
.linkset .LLNK76, sprintf.maxchanends $M printstr.maxchanends
.linkset worker_fx.maxchanends, .LLNK76
.linkset .LLNK77, sprintf.maxtimers $M printstr.maxtimers
.linkset worker_fx.maxtimers, .LLNK77
.linkset .LLNK81, sprintf.maxthreads - 1
.linkset .LLNK80, 1 + .LLNK81
.linkset .LLNK79, 1 $M .LLNK80
.linkset .LLNK83, printstr.maxthreads - 1
.linkset .LLNK82, 1 + .LLNK83
.linkset .LLNK78, .LLNK79 $M .LLNK82
.linkset worker_fx.maxthreads, .LLNK78
.cc_top buttonlistenertask.function,buttonlistenertask
          .align    4
.globwrite buttonlistenertask, iButton1, 0, 4, "../src/HW02-HotPotato.xc:127: error: previously used here (bytes 0..4)"
.call buttonlistenertask, __builtin_pins_eq
.call buttonlistenertask, __builtin_pins_eq
.globwrite buttonlistenertask, iButton1, 0, 4, "../src/HW02-HotPotato.xc:159: error: previously used here (bytes 0..4)"
.call buttonlistenertask, __builtin_timer_after
.set __builtin_pins_eq, 0
.linkset __builtin_pins_eq.locnoside, 0
.linkset __builtin_pins_eq.locnochandec, 1
.globl buttonlistenertask, "f{0}(chd,chd)"
.globl buttonlistenertask.nstackwords
.globl buttonlistenertask.maxthreads
.globl buttonlistenertask.maxtimers
.globl buttonlistenertask.maxchanends
.globl buttonlistenertask.maxsync
.type  buttonlistenertask, @function
.linkset buttonlistenertask.locnoside, 0
.linkset buttonlistenertask.locnochandec, 1
.linkset buttonlistenertask.nstackwords, 6
buttonlistenertask:
          entsp     0x6 
          stw       r0, sp[0x0] 
          stw       r1, sp[0x1] 
          getr      r0, 0x1
          stw       r0, sp[0x2] 
.L113:
.L114:
          ldc       r0, 0x0
          stw       r0, sp[0x4] 
.L115:
.L117:
          mkmsk     r1, 0x1
          ldw       r0, dp[iButton1] 
          setd      res[r0], r1
          ldw       r0, dp[iButton1] 
          setc      res[r0], 0x11
.L116:
          ldw       r0, dp[iButton1] 
.L183:
          in        r0, res[r0] 
.L119:
.L179:
          mkmsk     r0, 0x1
          bt        r0, .L120 
          bu        .L118 
.L120:
.L122:
.L123:
          ldw       r0, sp[0x2] 
          setc      res[r0], 0x1
          ldw       r0, sp[0x2] 
.L184:
          in        r0, res[r0] 
          stw       r0, sp[0x3] 
          ldw       r0, sp[0x3] 
          stw       r0, sp[0x3] 
.L124:
.L125:
          ldw       r1, sp[0x3] 
          ldw       r0, cp[.LC6]
          .section .cp.const4,     "acM", @progbits, 4
.cc_top .LC6.data, .LC6
          .align    4
.LC6:
          .int      0x00030d40

.cc_bottom .LC6.data
          .text
          add       r0, r1, r0
          stw       r0, sp[0x3] 
          clre      
          ldw       r0, sp[0x0] 
          ldap      r11, .L129
          setv      res[r0], r11
          ldw       r0, sp[0x0] 
          eeu       res[r0]
          ldw       r0, sp[0x1] 
          ldap      r11, .L144
          setv      res[r0], r11
          ldw       r0, sp[0x1] 
          eeu       res[r0]
          ldc       r1, 0x0
          ldw       r0, dp[iButton1] 
          setd      res[r0], r1
          ldw       r0, dp[iButton1] 
          setc      res[r0], 0x11
.L162:
          ldw       r0, dp[iButton1] 
          ldap      r11, .L159
          setv      res[r0], r11
          ldw       r0, dp[iButton1] 
          eeu       res[r0]
          ldw       r1, sp[0x3] 
          ldw       r0, sp[0x2] 
          setd      res[r0], r1
          ldw       r0, sp[0x2] 
          setc      res[r0], 0x9
.L174:
          ldw       r0, sp[0x2] 
          ldap      r11, .L171
          setv      res[r0], r11
          ldw       r0, sp[0x2] 
          eeu       res[r0]
.xtabranch .L129,.L171,.L159,.L144
          waiteu    
.L129:
          ldw       r0, sp[0x0] 
          chkct     res[r0], 0x1 
          ldw       r0, sp[0x0] 
          outct     res[r0], 0x1 
          ldw       r0, sp[0x0] 
.L185:
          in        r0, res[r0] 
          stw       r0, sp[0x5] 
          ldw       r0, sp[0x5] 
          stw       r0, sp[0x5] 
          ldw       r0, sp[0x0] 
          chkct     res[r0], 0x1 
          ldw       r0, sp[0x0] 
          outct     res[r0], 0x1 
.L132:
.L141:
          ldw       r0, sp[0x4] 
          bt        r0, .L134 
          bu        .L135 
.L134:
.L137:
.L138:
          ldw       r0, sp[0x0] 
          outct     res[r0], 0x1 
          ldw       r0, sp[0x0] 
          chkct     res[r0], 0x1 
          ldw       r1, sp[0x0] 
          ldw       r0, sp[0x5] 
.L186:
          out       res[r1], r0 
          ldw       r0, sp[0x0] 
          outct     res[r0], 0x1 
          ldw       r0, sp[0x0] 
          chkct     res[r0], 0x1 
.L139:
          ldc       r0, 0x0
          stw       r0, sp[0x4] 
          bu        .L133 
.L135:
.L140:
          ldw       r0, sp[0x1] 
          outct     res[r0], 0x1 
          ldw       r0, sp[0x1] 
          chkct     res[r0], 0x1 
          ldw       r1, sp[0x1] 
          ldw       r0, sp[0x5] 
.L187:
          out       res[r1], r0 
          ldw       r0, sp[0x1] 
          outct     res[r0], 0x1 
          ldw       r0, sp[0x1] 
          chkct     res[r0], 0x1 
.L133:
          bu        .L128 
.L144:
          ldw       r0, sp[0x1] 
          chkct     res[r0], 0x1 
          ldw       r0, sp[0x1] 
          outct     res[r0], 0x1 
          ldw       r0, sp[0x1] 
.L188:
          in        r0, res[r0] 
          stw       r0, sp[0x5] 
          ldw       r0, sp[0x5] 
          stw       r0, sp[0x5] 
          ldw       r0, sp[0x1] 
          chkct     res[r0], 0x1 
          ldw       r0, sp[0x1] 
          outct     res[r0], 0x1 
.L147:
.L156:
          ldw       r0, sp[0x4] 
          bt        r0, .L149 
          bu        .L150 
.L149:
.L152:
.L153:
          ldw       r0, sp[0x1] 
          outct     res[r0], 0x1 
          ldw       r0, sp[0x1] 
          chkct     res[r0], 0x1 
          ldw       r1, sp[0x1] 
          ldw       r0, sp[0x5] 
.L189:
          out       res[r1], r0 
          ldw       r0, sp[0x1] 
          outct     res[r0], 0x1 
          ldw       r0, sp[0x1] 
          chkct     res[r0], 0x1 
.L154:
          ldc       r0, 0x0
          stw       r0, sp[0x4] 
          bu        .L148 
.L150:
.L155:
          ldw       r0, sp[0x0] 
          outct     res[r0], 0x1 
          ldw       r0, sp[0x0] 
          chkct     res[r0], 0x1 
          ldw       r1, sp[0x0] 
          ldw       r0, sp[0x5] 
.L190:
          out       res[r1], r0 
          ldw       r0, sp[0x0] 
          outct     res[r0], 0x1 
          ldw       r0, sp[0x0] 
          chkct     res[r0], 0x1 
.L148:
          bu        .L128 
.L159:
          ldw       r0, dp[iButton1] 
.L191:
          in        r0, res[r0] 
.L163:
.L169:
          ldw       r0, sp[0x4] 
          bf        r0, .L165 
          bu        .L164 
.L165:
.L168:
          ldc       r0, 0x2
          stw       r0, sp[0x4] 
.L164:
          bu        .L128 
.L171:
          ldw       r0, sp[0x2] 
.L192:
          in        r0, res[r0] 
.L175:
.L176:
          ldw       r0, sp[0x2] 
          freer     res[r0]
.L181:
          retsp     0x6 
          bu        .L128 
.L126:
.L128:
          bu        .L119 
.L118:
          ldw       r0, sp[0x2] 
          freer     res[r0]
.L182:
          retsp     0x6 
.size buttonlistenertask, .-buttonlistenertask
.cc_bottom buttonlistenertask.function
.linkset buttonlistenertask.maxchanends, 0
.linkset buttonlistenertask.maxtimers, 1
.linkset buttonlistenertask.maxthreads, 1
.cc_top btn_sim.function,btn_sim
          .align    4
.globwrite btn_sim, oButtonDriver1, 0, 4, "../src/HW02-HotPotato.xc:185: error: previously used here (bytes 0..4)"
.call btn_sim, __builtin_timer_after
.globwrite btn_sim, oButtonDriver1, 0, 4, "../src/HW02-HotPotato.xc:194: error: previously used here (bytes 0..4)"
.call btn_sim, __builtin_timer_after
.globwrite btn_sim, oButtonDriver1, 0, 4, "../src/HW02-HotPotato.xc:202: error: previously used here (bytes 0..4)"
.globl btn_sim, "f{0}(0)"
.globl btn_sim.nstackwords
.globl btn_sim.maxthreads
.globl btn_sim.maxtimers
.globl btn_sim.maxchanends
.globl btn_sim.maxsync
.type  btn_sim, @function
.linkset btn_sim.locnoside, 0
.linkset btn_sim.locnochandec, 1
.linkset btn_sim.nstackwords, 2
btn_sim:
          entsp     0x2 
          getr      r0, 0x1
          stw       r0, sp[0x0] 
.L193:
.L194:
          ldw       r1, dp[oButtonDriver1] 
          mkmsk     r0, 0x1
.L213:
          out       res[r1], r0 
.L195:
.L196:
          ldw       r0, sp[0x0] 
          setc      res[r0], 0x1
          ldw       r0, sp[0x0] 
.L214:
          in        r0, res[r0] 
          stw       r0, sp[0x1] 
          ldw       r0, sp[0x1] 
          stw       r0, sp[0x1] 
.L197:
.L198:
          ldw       r1, sp[0x1] 
          ldc       r0, 0x64
          add       r0, r1, r0
          stw       r0, sp[0x1] 
.L199:
.L201:
          ldw       r1, sp[0x1] 
          ldw       r0, sp[0x0] 
          setd      res[r0], r1
          ldw       r0, sp[0x0] 
          setc      res[r0], 0x9
.L200:
          ldw       r0, sp[0x0] 
.L215:
          in        r0, res[r0] 
.L202:
.L203:
          ldw       r1, dp[oButtonDriver1] 
          ldc       r0, 0x0
.L216:
          out       res[r1], r0 
.L204:
.L205:
          ldw       r0, sp[0x0] 
          setc      res[r0], 0x1
          ldw       r0, sp[0x0] 
.L217:
          in        r0, res[r0] 
          stw       r0, sp[0x1] 
          ldw       r0, sp[0x1] 
          stw       r0, sp[0x1] 
.L206:
.L207:
          ldw       r1, sp[0x1] 
          ldc       r0, 0x64
          add       r0, r1, r0
          stw       r0, sp[0x1] 
.L208:
.L210:
          ldw       r1, sp[0x1] 
          ldw       r0, sp[0x0] 
          setd      res[r0], r1
          ldw       r0, sp[0x0] 
          setc      res[r0], 0x9
.L209:
          ldw       r0, sp[0x0] 
.L218:
          in        r0, res[r0] 
.L211:
          ldw       r1, dp[oButtonDriver1] 
          mkmsk     r0, 0x1
.L219:
          out       res[r1], r0 
          ldw       r0, sp[0x0] 
          freer     res[r0]
.L212:
          retsp     0x2 
.size btn_sim, .-btn_sim
.cc_bottom btn_sim.function
.linkset btn_sim.maxchanends, 0
.linkset btn_sim.maxtimers, 1
.linkset btn_sim.maxthreads, 1
.par btn_sim, worker, "../src/HW02-HotPotato.xc:30: error: use of `%s' violates parallel usage rules"
.par btn_sim, buttonlistenertask, "../src/HW02-HotPotato.xc:30: error: use of `%s' violates parallel usage rules"
.par worker, worker, "../src/HW02-HotPotato.xc:30: error: use of `%s' violates parallel usage rules"
.par worker, buttonlistenertask, "../src/HW02-HotPotato.xc:30: error: use of `%s' violates parallel usage rules"
# Thread names for recovering thread graph in linker
.set thread.anon.0, 0  #unreal
.set thread.anon.1, 0  #unreal
.set thread.anon.2, 0  #unreal
.set thread.anon.3, 0  #unreal
.set thread.anon.4, 0  #unreal
.set thread.anon.5, 0  #unreal
.set thread.anon.6, 0  #unreal
.set thread.anon.7, 0  #unreal
.set thread.anon.8, 0  #unreal
.set thread.anon.9, 0  #unreal
.set thread.anon.10, 0  #unreal
.extern __builtin_getid, "f{si}(0)"
.extern stdcore, "a(1:cr)"
.extern __builtin_getid, "f{si}(0)"
          .section .xtaendpointtable,       "", @progbits
.L220:
          .int      .L221-.L220
          .int      0x00000000
          .asciiz   "/home/joseph/School/comp/joslewis/HW02-HotPotato/.build_Debug"
.cc_top btn_sim.function, btn_sim
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x000000ca
          .long    .L219
.cc_bottom btn_sim.function
.cc_top btn_sim.function, btn_sim
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x000000c7
          .long    .L218
.cc_bottom btn_sim.function
.cc_top btn_sim.function, btn_sim
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x000000c5
          .long    .L217
.cc_bottom btn_sim.function
.cc_top btn_sim.function, btn_sim
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x000000c2
          .long    .L216
.cc_bottom btn_sim.function
.cc_top btn_sim.function, btn_sim
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x000000bf
          .long    .L215
.cc_bottom btn_sim.function
.cc_top btn_sim.function, btn_sim
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x000000bd
          .long    .L214
.cc_bottom btn_sim.function
.cc_top btn_sim.function, btn_sim
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x000000b9
          .long    .L213
.cc_bottom btn_sim.function
.cc_top buttonlistenertask.function, buttonlistenertask
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x000000a4
          .long    .L192
.cc_bottom buttonlistenertask.function
.cc_top buttonlistenertask.function, buttonlistenertask
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x0000009f
          .long    .L191
.cc_bottom buttonlistenertask.function
.cc_top buttonlistenertask.function, buttonlistenertask
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x0000009c
          .long    .L190
.cc_bottom buttonlistenertask.function
.cc_top buttonlistenertask.function, buttonlistenertask
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000098
          .long    .L189
.cc_bottom buttonlistenertask.function
.cc_top buttonlistenertask.function, buttonlistenertask
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000095
          .long    .L188
.cc_bottom buttonlistenertask.function
.cc_top buttonlistenertask.function, buttonlistenertask
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000093
          .long    .L187
.cc_bottom buttonlistenertask.function
.cc_top buttonlistenertask.function, buttonlistenertask
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x0000008f
          .long    .L186
.cc_bottom buttonlistenertask.function
.cc_top buttonlistenertask.function, buttonlistenertask
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x0000008c
          .long    .L185
.cc_bottom buttonlistenertask.function
.cc_top buttonlistenertask.function, buttonlistenertask
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000086
          .long    .L184
.cc_bottom buttonlistenertask.function
.cc_top buttonlistenertask.function, buttonlistenertask
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x0000007f
          .long    .L183
.cc_bottom buttonlistenertask.function
.cc_top worker_fx.function, worker_fx
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000062
          .long    .L112
.cc_bottom worker_fx.function
.cc_top worker_fx.function, worker_fx
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x0000005e
          .long    .L111
.cc_bottom worker_fx.function
.cc_top worker_fx.function, worker_fx
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x0000005c
          .long    .L110
.cc_bottom worker_fx.function
.cc_top worker.function, worker
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000045
          .long    .L83
.cc_bottom worker.function
.cc_top worker.function, worker
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000041
          .long    .L81
.cc_bottom worker.function
.cc_top worker.function, worker
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x0000003d
          .long    .L79
.cc_bottom worker.function
.cc_top worker.function, worker
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000038
          .long    .L78
.cc_bottom worker.function
.cc_top worker.function, worker
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000032
          .long    .L77
.cc_bottom worker.function
.L221:
          .section .xtacalltable,       "", @progbits
.L222:
          .int      .L223-.L222
          .int      0x00000000
          .asciiz   "/home/joseph/School/comp/joslewis/HW02-HotPotato/.build_Debug"
.cc_top worker_fx.function, worker_fx
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000054
          .long    .L109
.cc_bottom worker_fx.function
.cc_top worker_fx.function, worker_fx
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000053
          .long    .L108
.cc_bottom worker_fx.function
.cc_top worker.function, worker
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000042
          .long    .L82
.cc_bottom worker.function
.cc_top worker.function, worker
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x0000003e
          .long    .L80
.cc_bottom worker.function
.cc_top main.function, main
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000021
          .long    .L21
.cc_bottom main.function
.cc_top main.function, main
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000022
          .long    .L20
.cc_bottom main.function
.cc_top main.function, main
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000023
          .long    .L19
.cc_bottom main.function
.cc_top main.function, main
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000025
          .long    .L18
.cc_bottom main.function
.cc_top main.function, main
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000020
          .long    .L17
.cc_bottom main.function
.L223:
          .section .xtalabeltable,       "", @progbits
.L224:
          .int      .L225-.L224
          .int      0x00000000
          .asciiz   "/home/joseph/School/comp/joslewis/HW02-HotPotato/.build_Debug"
.cc_top btn_sim.function, btn_sim
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x000000cd
          .int      0x000000cd
# line info for line 205 
          .long    .L212
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x000000ca
          .int      0x000000ca
# line info for line 202 
          .long    .L211
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x000000c7
          .int      0x000000c7
# line info for line 199 
          .long    .L210
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x000000c6
          .int      0x000000c6
# line info for line 198 
          .long    .L207
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x000000c5
          .int      0x000000c5
# line info for line 197 
          .long    .L205
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x000000c2
          .int      0x000000c2
# line info for line 194 
          .long    .L203
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x000000bf
          .int      0x000000bf
# line info for line 191 
          .long    .L201
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x000000be
          .int      0x000000be
# line info for line 190 
          .long    .L198
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x000000bd
          .int      0x000000bd
# line info for line 189 
          .long    .L196
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x000000b9
          .int      0x000000b9
# line info for line 185 
          .long    .L194
.cc_bottom btn_sim.function
.cc_top buttonlistenertask.function, buttonlistenertask
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x000000a9
          .int      0x000000a9
# line info for line 169 
          .long    .L182
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x000000a9
          .int      0x000000a9
# line info for line 169 
          .long    .L181
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x000000a5
          .int      0x000000a5
# line info for line 165 
          .long    .L176
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x000000a1
          .int      0x000000a1
# line info for line 161 
          .long    .L168
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x000000a0
          .int      0x000000a0
# line info for line 160 
          .long    .L169
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x0000009c
          .int      0x0000009c
# line info for line 156 
          .long    .L155
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000099
          .int      0x00000099
# line info for line 153 
          .long    .L154
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000098
          .int      0x00000098
# line info for line 152 
          .long    .L153
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000096
          .int      0x00000096
# line info for line 150 
          .long    .L156
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000093
          .int      0x00000093
# line info for line 147 
          .long    .L140
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000090
          .int      0x00000090
# line info for line 144 
          .long    .L139
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x0000008f
          .int      0x0000008f
# line info for line 143 
          .long    .L138
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x0000008d
          .int      0x0000008d
# line info for line 141 
          .long    .L141
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000087
          .int      0x00000087
# line info for line 135 
          .long    .L125
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000086
          .int      0x00000086
# line info for line 134 
          .long    .L123
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000082
          .int      0x00000082
# line info for line 130 
          .long    .L179
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x0000007f
          .int      0x0000007f
# line info for line 127 
          .long    .L117
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x0000007c
          .int      0x0000007c
# line info for line 124 
          .long    .L114
.cc_bottom buttonlistenertask.function
.cc_top worker_fx.function, worker_fx
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000066
          .int      0x00000066
# line info for line 102 
          .long    .L107
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000065
          .int      0x00000065
# line info for line 101 
          .long    .L105
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000062
          .int      0x00000062
# line info for line 98 
          .long    .L103
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000061
          .int      0x00000061
# line info for line 97 
          .long    .L104
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x0000005e
          .int      0x0000005e
# line info for line 94 
          .long    .L98
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x0000005d
          .int      0x0000005d
# line info for line 93 
          .long    .L95
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x0000005c
          .int      0x0000005c
# line info for line 92 
          .long    .L93
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000057
          .int      0x00000057
# line info for line 87 
          .long    .L91
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000054
          .int      0x00000054
# line info for line 84 
          .long    .L89
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000053
          .int      0x00000053
# line info for line 83 
          .long    .L86
.cc_bottom worker_fx.function
.cc_top worker.function, worker
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x0000004a
          .int      0x0000004a
# line info for line 74 
          .long    .L76
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x0000004a
          .int      0x0000004a
# line info for line 74 
          .long    .L75
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000046
          .int      0x00000046
# line info for line 70 
          .long    .L68
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x0000004a
          .int      0x0000004a
# line info for line 74 
          .long    .L74
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000043
          .int      0x00000043
# line info for line 67 
          .long    .L59
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000042
          .int      0x00000042
# line info for line 66 
          .long    .L61
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x0000004a
          .int      0x0000004a
# line info for line 74 
          .long    .L73
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x0000003f
          .int      0x0000003f
# line info for line 63 
          .long    .L47
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x0000003e
          .int      0x0000003e
# line info for line 62 
          .long    .L49
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000039
          .int      0x00000039
# line info for line 57 
          .long    .L35
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000038
          .int      0x00000038
# line info for line 56 
          .long    .L33
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000036
          .int      0x00000036
# line info for line 54 
          .long    .L71
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000032
          .int      0x00000032
# line info for line 50 
          .long    .L26
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000031
          .int      0x00000031
# line info for line 49 
          .long    .L27
.cc_bottom worker.function
.cc_top main.function, main
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000027
          .int      0x00000027
# line info for line 39 
          .long    .L16
          .asciiz  "../src/HW02-HotPotato.xc"
          .int      0x00000020
          .int      0x00000020
# line info for line 32 
          .long    .L1
.cc_bottom main.function
.L225:
          .section .dp.data,       "adw", @progbits
.align 4
          .align    4
          .section .dp.bss,        "adw", @nobits
.align 4
          .ident    "XMOS 32-bit XC Compiler 11.11.0 (build 2237)"
          .core     "XS1"
          .corerev  "REVB"
