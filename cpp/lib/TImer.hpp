/*
 * Copyright 2014 Joseph Lewis <joseph@josephlewis.net>
 *
 * This file is part of University of Denver Autopilot.
 * Dual licensed under the GPL v 3 and the Apache 2.0 License
 */


#ifndef TIMER_HPP
#define TIMER_HPP

#include <chrono>
#include <mutex>

/** Provides a basic timing mechanism for various classes.

**/
class Timer
{
    private:
        /// Locks the start time
        mutable std::mutex start_time_lock;
        /// Keeps the time that the timer was initiated
        std::chrono::time_point<std::chrono::high_resolution_clock> _timerInit;
    public:
        Timer()
        :_timerInit(std::chrono::high_resolution_clock::now())
        {}

    /// set the start_time to the current time
    void set_start_time()
    {
        std::lock_guard<std::mutex> lock(start_time_lock);
        _timerInit = std::chrono::high_resolution_clock::now();
    }
    /// get the start_Time
    std::chrono::time_point<std::chrono::high_resolution_clock> get_start_time() const
    {
        std::lock_guard<std::mutex> lock(start_time_lock);
        return _timerInit;
    }

    /// Get the number of milliseconds since this timer was started or the set_start_time was called
    long getMsSinceInit() const
    {
        std::lock_guard<std::mutex> lock(start_time_lock);
        return std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::high_resolution_clock::now() - _timerInit).count();
    }

    /// Acts like a stopwatch button, reutrns the number of milliseconds since the last "click" and inits the timer again
    long click()
    {
        std::lock_guard<std::mutex> lock(start_time_lock);
        auto now = std::chrono::high_resolution_clock::now();
        long ms = std::chrono::duration_cast<std::chrono::milliseconds>(now - _timerInit).count();
        _timerInit = now;
        return ms;
    }
};

#endif //TIMER_HPP

