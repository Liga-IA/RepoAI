/*
 * vector_queue.h
 *
 *  Created on: Sep 16, 2020
 *      Author: Matuzalem Muller
 */

#ifndef LIB_VECTOR_QUEUE_H_
#define LIB_VECTOR_QUEUE_H_

#include <vector>
#include <cstdint>

/**
 * Implementation of queue class using STL vector.
 * Class provides flexibility on adding elements to the front and back of the
 * queue.
 */
template <class X>
class VectorQueue
{
  std::vector<X> _queue;
  std::uint8_t _capacity;

public:
  void init(std::uint8_t size);
  void push_front(X item);
  void push_back(X item);
  void pop_back();
  X * front();
  X * back();
  X * item_at(std::uint8_t index);
  void erase(std::uint8_t index);
  void rotate();
  std::uint8_t size();
  bool is_empty();
  bool is_full();
};

/**
 * Configure queue before using class
 * @param size Max size of queue
 */
template <class X>
void VectorQueue<X>::init(std::uint8_t size)
{
  _capacity = size;
  _queue.reserve(size);
}

/**
 * Add element to the front of the queue
 * @param item Element to be added
 */
template <class X>
void VectorQueue<X>::push_front(X item)
{
  if (_queue.size() < _capacity)
  {
    _queue.insert(_queue.begin(), item);
  }
}

/**
 * Add element to the back of the queue
 * @param item Element to be added
 */
template <class X>
void VectorQueue<X>::push_back(X item)
{
  if (_queue.size() < _capacity)
  {
    _queue.push_back(item);
  }
}

/**
 * Remove element from the back of the queue
 */
template <class X>
void VectorQueue<X>::pop_back()
{
  _queue.pop_back();
}

/**
 * Returns pointer to element at the front of the queue
 * @return Pointer to element at the front of the queue
 */
template <class X>
X * VectorQueue<X>::front()
{
  return &_queue.front();
}

/**
 * Returns pointer to element at the back of the queue
 * @return Pointer to element at the back of the queue
 */
template <class X>
X * VectorQueue<X>::back()
{
  if (_queue.size() > 0)
  {
    return &_queue.back();
  }
  else
  {
    return nullptr;
  }
}

/**
 * Returns pointer to element at index position from the queue
 * @param index Index of the queue
 * @result Pointer to element at given index
 */
template <class X>
X * VectorQueue<X>::item_at(std::uint8_t index)
{
  if (_queue.size() > index)
  {
    return &_queue.at(index);
  }
  else
  {
    return nullptr;
  }
}

/**
 * Erase element at specific position of queue
 * @param index Position of element to be deleted
 */
template <class X>
void VectorQueue<X>::erase(std::uint8_t index)
{
  if (_queue.size() > index)
  {
    _queue.erase(_queue.begin()+index);
  }
}

/**
 * Places last element from queue in the begin of the queue
 */
template <class X>
void VectorQueue<X>::rotate()
{
  if (_queue.size() > 1)
  {
    X item(_queue.back());
    _queue.pop_back();
    _queue.insert(_queue.begin(), item);
  }
}

/**
 * Return the size of the queue
 * @result Size/number of elements of queue
 */
template <class X>
std::uint8_t VectorQueue<X>::size()
{
  return _queue.size();
}

/**
 * Checks if the queue is empty
 * @result false if queue is full of elements, true otherwise
 */
template <class X>
bool VectorQueue<X>::is_empty()
{
  return (_queue.size() == 0);
}

/**
 * Checks if the queue is full
 * @result true if queue is full of elements, false otherwise
 */
template <class X>
bool VectorQueue<X>::is_full()
{
  return (_queue.size() == _capacity);
}

#endif /* LIB_VECTOR_QUEUE_H_ */
