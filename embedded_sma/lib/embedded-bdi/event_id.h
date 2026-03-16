/*
 * event_id.h
 *
 *  Created on: Jul 10, 2020
 *      Author: Matuzalem Muller
 */

#ifndef LIB_EVENT_ID_H_
#define LIB_EVENT_ID_H_

#include <cstdint>

/**
 * Represents Event Unique Identifier.
 * Class can be modified to use other control and data representation such as
 * UUID for better handling of events.
 */
class EventID
{
private:
  /// Unique Event identifier
  std::uint8_t _id = 0;

protected:
  static std::uint8_t id;

public:
  /**
   * EventID constructor. Starts _id with unique identifier based on the
   * static ID.
   */
  EventID();

  /**
   * Compares given ID with object _id
   * @return True if event_id is equal to object _id, false otherwise
   */
  bool is_equal(EventID * event_id);

  const std::uint8_t get_id() const
  {
    return _id;
  }

  /**
   * Returns EventID's main counter
   * @return id
   */
  static std::uint8_t get_control_id()
  {
    return EventID::id;
  }
};

#endif /* LIB_EVENT_ID_H_ */

