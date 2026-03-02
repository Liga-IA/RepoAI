#include <Arduino.h>
#include "agent.h"
#include "configuration.h"
#include "functions.h"
#include "espnow_manager.h"

// --- Hardware Setup ---
const int LED_PIN = 15;

// --- Global Variables ---
AgentSettings settings;
Agent agent(
    settings.get_belief_base(),
    settings.get_event_base(),
    settings.get_plan_base(),
    settings.get_intention_base()
);
ESPNowManager espnow_manager;
uint8_t last_requester_mac[6] = {0};

// Manual Timers
unsigned long last_discovery_time = 0;
unsigned long last_cleanup_time = 0;
unsigned long last_print_time = 0;

// --- Action Functions ---
void setup_actions() {
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  Serial.println("[SETUP] Actions (LED) initialized.");
}

bool action_show_ready_message() {
  Serial.println("[ACTION] LED Agent ready for cooperation.");
  return true;
}

bool action_led_on() {
  Serial.println("[ACTION] Plan to turn ON LED activated. Turning ON LED now!");
  digitalWrite(LED_PIN, HIGH);
  return true;
}

bool action_led_off() {
  Serial.println("[ACTION] Plan to turn OFF LED activated. Turning OFF LED now!");
  digitalWrite(LED_PIN, LOW);
  return true;
}

bool action_send_cooperation_response() {
  Serial.println("[COOPERATION] Sending confirmation response...");
  return espnow_manager.send_cooperation_response(last_requester_mac, 1, true);
}

// --- ESP-NOW Callback ---
void on_message_received(const uint8_t* mac_addr, const uint8_t* data, int len) {
    NetworkMessage_t msg;
    if (len > sizeof(NetworkMessage_t)) return;
    memcpy(&msg, data, len);
    if (memcmp(msg.sender_mac, espnow_manager.get_agent_mac(), 6) == 0) return;
    
    if (msg.type == MSG_DISCOVERY) {
        espnow_manager.add_or_update_neighbor(msg.sender_mac, msg.payload[0]);
    } 
    else if (msg.type == MSG_COOPERATION_REQUEST) {
        CooperationAction_t received_action;
        memcpy(&received_action, msg.payload, sizeof(CooperationAction_t));

        if (received_action.action_type == 1) { // Turn On
            Serial.println("[NETWORK] Turn ON message received! Generating BDI event...");
            memcpy(last_requester_mac, msg.sender_mac, 6);
            settings.get_event_base()->add_event(Event(EventOperator::BELIEF_ADDITION, Proposition(3)));
        } 
        else if (received_action.action_type == 2) { // Turn Off
            Serial.println("[NETWORK] Turn OFF message received! Generating BDI event...");
            settings.get_event_base()->add_event(Event(EventOperator::BELIEF_ADDITION, Proposition(5)));
        }
    }
}

// --- Setup ---
void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("\n=== Starting LED Agent (Actuator) ===");
  setup_actions();
  
  if (!espnow_manager.initialize("LEDAgent", CAP_ACTUATOR_LED, on_message_received)) {
    while(1) delay(1000);
  }

  espnow_manager.start();
  Serial.println("=== System started successfully! ===");
}

// --- Main Loop ---
void loop() {
  unsigned long current_time = millis();

  if (current_time - last_discovery_time > DISCOVERY_INTERVAL_MS) {
    last_discovery_time = current_time;
    espnow_manager.send_discovery_broadcast();
  }
  if (current_time - last_cleanup_time > NEIGHBOR_TIMEOUT_MS) {
    last_cleanup_time = current_time;
    espnow_manager.cleanup_neighbors();
  }

  if (current_time - last_print_time > 10000) {
    last_print_time = current_time;
    espnow_manager.print_neighbor_table();
  }

  agent.run();
  delay(100);
}