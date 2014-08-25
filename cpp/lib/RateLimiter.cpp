/**************************************************************************
 * Copyright 2013 Joseph Lewis <joehms22@gmail.com>
 *
 * This file is part of ANCL Autopilot.
 *
 *     ANCL Autopilot is free software: you can redistribute it and/or modify
 *     it under the terms of the GNU General Public License as published by
 *     the Free Software Foundation, either version 3 of the License, or
 *     (at your option) any later version.
 *
 *     ANCL Autopilot is distributed in the hope that it will be useful,
 *     but WITHOUT ANY WARRANTY; without even the implied warranty of
 *     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *     GNU General Public License for more details.
 *
 *     You should have received a copy of the GNU General Public License
 *     along with ANCL Autopilot.  If not, see <http://www.gnu.org/licenses/>.
 *************************************************************************/

#include "RateLimiter.h"

#include <iostream>
#include <thread>

#include "Debug.h"

Logger rateLimiterLogger("RateLimiter");

//#define NDEBUG

RateLimiter::RateLimiter(int hz, bool ckload)
    :_msToWait(1000 / hz),
     _nextTime(),
    _checkload(ckload),
    _msPerLoop(1000.0 / hz)
{
    _nextTime = std::chrono::high_resolution_clock::now();
    _nextTime = _nextTime + _msToWait;
}

RateLimiter::~RateLimiter()
{
}

float RateLimiter::wait()
{
    float ret = 0;

    if(_checkload)
    {
        std::chrono::high_resolution_clock::time_point const now = std::chrono::high_resolution_clock::now();
        float used = std::chrono::duration_cast<std::chrono::milliseconds>(now - _nextTime).count() + _msPerLoop;
        ret = used / _msPerLoop;
    }

    std::chrono::high_resolution_clock::time_point const timeout = _nextTime;
    std::this_thread::sleep_until(timeout);
    _nextTime += _msToWait;

#ifndef NDEBUG
    if(std::chrono::high_resolution_clock::now() > _nextTime)
    {
        rateLimiterLogger.warning() << "RateLimiter: Fallen behind!";
    }
#endif

    return ret;
}

void RateLimiter::finishedCriticalSection()
{
    // yield the thread so others can execute now.
    std::this_thread::yield();
}


