/*
 * event.cpp
 *
 *  Created on: May 25, 2020
 *      Author: Matuzalem Muller
 */

#include "event.h"

Event::Event() {}

Event::Event(EventOperator op, Proposition prop)
{
   _operator = op;
   _proposition = prop;
}
