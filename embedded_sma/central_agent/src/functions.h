#ifndef FUNCTIONS_H_
#define FUNCTIONS_H_

void setup_actions();
bool action_show_ready_message();

// Funções de cooperação
bool action_request_cooperation_on();
bool action_request_cooperation_off();
bool action_send_cooperation_response();
bool action_sound_buzzer();

#endif /* FUNCTIONS_H_ */