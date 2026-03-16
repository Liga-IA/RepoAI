/*
 * event_id.cpp
 *
 *  Created on: Jul 10, 2020
 *      Author: matuzalem
 */

#include "event_id.h"

std::uint8_t EventID::id = 0;

EventID::EventID()
{
  _id = id++;
}

bool EventID::is_equal(EventID * event_id)
{
  return (_id == event_id->_id);
}
