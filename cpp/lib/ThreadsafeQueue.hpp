/**************************************************************************
 * Copyright 2013 Joseph Lewis III <joehms22@gmail.com>
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


#ifndef COMMANDQUEUE_H_
#define COMMANDQUEUE_H_

#include <queue>
#include <mutex>

/// A threadsafe queue
template<class T>
class ThreadQueue
{
private:
    /// the queue
    std::queue<T> _queue;

    /// mutex for the queue
    mutable std::mutex _queue_lock;

public:

    ThreadQueue();
    virtual ~ThreadQueue();

    void push(T val);
    T pop();
    bool empty();
    int size();
};

template<class T>
ThreadQueue<T>::ThreadQueue()
{
}

template<class T>
ThreadQueue<T>::~ThreadQueue()
{
}


template<class T>
T ThreadQueue<T>::pop()
{
    std::lock_guard<std::mutex> lock(_queue_lock);
    T value = _queue.front();
    _queue.pop();
    return value;
}

template<class T>
void ThreadQueue<T>::push(T value)
{
    std::lock_guard<std::mutex> lock(_queue_lock);
    _queue.push(value);
}

template<class T>
bool ThreadQueue<T>::empty()
{
    std::lock_guard<std::mutex> lock(_queue_lock);
    return _queue.empty();
}

template<class T>
int ThreadQueue<T>::size()
{
    std::lock_guard<std::mutex> lock(_queue_lock);
    return _queue.size();
}


#endif /* COMMANDQUEUE_H_ */
