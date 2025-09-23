/*
 * event.h
 *
 *  Created on: May 25, 2020
 *      Author: Matuzalem Muller
 */

#ifndef SYNTAX_EVENT_H_
#define SYNTAX_EVENT_H_

#include "proposition.h"
#include "event_operator.h"
#include "event_id.h"
#include <cstdint>

/**
 * Represents events for belief updates and plan adoption/drop.
 */
class Event
{
private:
  EventOperator _operator;
  Proposition _proposition;
  /// Event identifier
  EventID _id;

public:
  Event();

  /**
   * Event constructor
   * @param op Event's EventOperator
   * @param prop Event's Proposition
   */
  Event(EventOperator op, Proposition prop);

  const EventOperator & get_operator() const
  {
    return _operator;
  }

  const Proposition & get_proposition() const
  {
    return _proposition;
  }

  /**
   * Unique ID given to Event
   * @return returns pointer to EventID
   */
  EventID * get_event_id()
  {
    return &_id;
  }
};


#endif /* SYNTAX_EVENT_H_ */
