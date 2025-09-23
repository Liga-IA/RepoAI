/*
 * event_base.h
 *
 *  Created on: May 31, 2020
 *      Author: Matuzalem Muller
 */

#ifndef BDI_EVENT_BASE_H_
#define BDI_EVENT_BASE_H_

#include "event.h"
#include "vector_queue.h"
#include <cstdint>

/**
 * Collection of agent events.
 */
class EventBase
{
private:
  /// Vector of Events
  VectorQueue<Event> _pending_events;
  /// Max size of _belief_base vector
  std::uint8_t _size = 0;

public:
  EventBase();

  /**
   * EventBase's constructor
   * @param size Size of EventBase buffer
   */
  EventBase(std::uint8_t size);

  /**
   * Creates an Event using op and prop and adds Event _pending_events
   * @param event Event to be added to _pending_events
   * @return true if event is added to _pending_events, false otherwise
   */
  bool add_event(Event event);

  /**
   * Removes Event from _pending_events and returns pointer to removed Event
   * @return Pointer to first element from _pending_events. If _pending_events
   * has no elements, return is nullptr
   */
  Event get_event();

  /**
   * Returns last Event added to EventBase
   * @return Pointer to last Event added to _pending_events
   */
  Event * last_event();

  /**
   * Check if Event exists in EventBase given event_id
   * @param event_id EventID to be checked
   * @return True if Event exists in _pending_events, false otherwise
   */
  bool event_exists(EventID * event_id);

  /**
   * Returns if EventBase is full based on _pending_events size
   * @return true if EventBase is full, false otherwise
   */
  bool is_full();

  /**
   * Returns if EventBase is empty based on _pending_events size
   * @return true if EventBase is empty, false otherwise
   */
  bool is_empty();

  Event * get_event_by_id(EventID * event);
};

#endif /* BDI_EVENT_BASE_H_ */
