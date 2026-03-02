#include <Arduino.h>
#include "configuration.h"
#include "agent.h"
#include "espnow_manager.h"
#include "functions.h"
#include <DHT.h>
// #include <IRremoteESP8266.h>

// --- Pins and Parameters ---
const int LDR_PIN = 2;
const int LDR_THRESHOLD = 540;
const int BUZZER_PIN = 7;
const int POT_PIN = 1;
const int POT_THRESHOLD = 500;
const int LM35_PIN = 3;
const int DHT_PIN = 6;
// const int IR_PIN = 8;

// --- Sensor Objects ---
#define DHTTYPE DHT11
DHT dht(DHT_PIN, DHTTYPE);
// IRrecv irrecv(IR_PIN);
// decode_results results;

// --- Agent Setup ---
AgentSettings settings;
Agent agent(
    settings.get_belief_base(),
    settings.get_event_base(),
    settings.get_plan_base(),
    settings.get_intention_base()
);
ESPNowManager espnow_manager;

// --- Manual Timers and State Variables ---
unsigned long last_discovery_time = 0;
unsigned long last_cleanup_time = 0;
unsigned long last_sensor_read_time = 0;
unsigned long last_print_time = 0;
unsigned long last_belief_sync_time = 0;

static bool last_ldr_state = false;
static bool has_neighbor_belief = false;
static bool last_hot_state = false;
static bool last_humid_state = false;
static bool last_pot_high_state = false;

// --- Hardware and Action Functions ---
void setup_hardware() {
  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(BUZZER_PIN, LOW);
  pinMode(LDR_PIN, INPUT);
  pinMode(POT_PIN, INPUT);
  pinMode(LM35_PIN, INPUT);
  
  dht.begin();
  // irrecv.enableIRIn();
  
  Serial.println("[SETUP] Hardware initialized (Buzzer, LDR, POT, LM35, DHT).");
}

bool action_show_ready_message() {
  Serial.println("[ACTION] Central Agent (Sensor+Actuator) ready.");
  return true;
}

bool action_sound_buzzer() {
  Serial.println("[ACTION] Alarm request received! Sounding BUZZER.");
  tone(BUZZER_PIN, 1000, 200); // 200ms beep
  return true;
}

bool action_request_cooperation_on() {
  NeighborEntry_t led_neighbor;
  if (espnow_manager.find_neighbor_by_capability(CAP_ACTUATOR_LED, &led_neighbor)) {
    CooperationAction_t action_request;
    action_request.action_type = 1; // 1 = Turn ON LED
    return espnow_manager.send_cooperation_request(led_neighbor.mac, &action_request);
  }
  return false;
}

bool action_request_cooperation_off() {
  NeighborEntry_t led_neighbor;
  if (espnow_manager.find_neighbor_by_capability(CAP_ACTUATOR_LED, &led_neighbor)) {
    CooperationAction_t action_request;
    action_request.action_type = 2; // 2 = Turn OFF LED
    return espnow_manager.send_cooperation_request(led_neighbor.mac, &action_request);
  }
  return false;
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

        if (received_action.action_type == 3) { // 3 = Sound Alarm
            Serial.println("[NETWORK] ALARM request received! Generating BDI event...");
            settings.get_event_base()->add_event(Event(EventOperator::BELIEF_ADDITION, Proposition(1)));
        }
    }
}

// --- Setup ---
void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("=== Starting Central Agent ===");
  setup_hardware();

  uint8_t capabilities = CAP_SENSOR_LIGHT | CAP_ACTUATOR_BUZZER | CAP_SENSOR_TEMP_HUMID | CAP_SENSOR_TEMP_ANALOG | CAP_SENSOR_POT; // CAP_SENSOR_IR temporarily removed
  if(!espnow_manager.initialize("CentralAgent", capabilities, on_message_received)) {
      while(1) delay(1000);
  }
  espnow_manager.start();
  Serial.println("=== System started successfully ===");
}

// --- Main Loop ---
void loop() {
  unsigned long current_time = millis();

  // Read all sensors
  if (current_time - last_sensor_read_time > 2000) { // Reading every 2 seconds
    last_sensor_read_time = current_time;

    // LDR
    bool is_dark = analogRead(LDR_PIN) < LDR_THRESHOLD;
    if (is_dark != last_ldr_state) {
      last_ldr_state = is_dark;
      if (is_dark) {
        Serial.println("[EVENT] Belief added: low_light (true)");
        settings.get_event_base()->add_event(Event(EventOperator::BELIEF_ADDITION, Proposition(0)));
      } else {
        Serial.println("[EVENT] Belief deleted: low_light (false)");
        settings.get_event_base()->add_event(Event(EventOperator::BELIEF_DELETION, Proposition(0)));
      }
    }

    // Potentiometer
    int pot_value = analogRead(POT_PIN);
    Serial.printf("[SENSOR] Potentiometer: %d\n", pot_value);
    bool is_pot_high = pot_value > POT_THRESHOLD;
    if (is_pot_high != last_pot_high_state) {
        last_pot_high_state = is_pot_high;
        if (is_pot_high) {
            Serial.println("[EVENT] Belief added: pot_is_high (true)");
            settings.get_event_base()->add_event(Event(EventOperator::BELIEF_ADDITION, Proposition(8)));
        } else {
            Serial.println("[EVENT] Belief deleted: pot_is_high (false)");
            settings.get_event_base()->add_event(Event(EventOperator::BELIEF_DELETION, Proposition(8)));
        }
    }

    // LM35
    int lm35_raw = analogRead(LM35_PIN);
    float lm35_temp = (lm35_raw / 4095.0) * 330; // For 3.3V ADC
    Serial.printf("[SENSOR] LM35: %.2f C\n", lm35_temp);
    bool is_hot = lm35_temp > 28.0;
    if (is_hot != last_hot_state) {
        last_hot_state = is_hot;
        if(is_hot) {
          Serial.println("[EVENT] Belief added: is_hot (true)");
          settings.get_event_base()->add_event(Event(EventOperator::BELIEF_ADDITION, Proposition(5)));
        } else {
          Serial.println("[EVENT] Belief deleted: is_hot (false)");
          settings.get_event_base()->add_event(Event(EventOperator::BELIEF_DELETION, Proposition(5)));
        }
      }

    // DHT11
    float dht_humidity = dht.readHumidity();
    float dht_temp = dht.readTemperature();
    if (!isnan(dht_humidity) && !isnan(dht_temp)) {
      Serial.printf("[SENSOR] DHT11: %.1f%% Humidity, %.1f C Temperature\n", dht_humidity, dht_temp);
      
      bool is_hot = dht_temp > 28.0;
      if (is_hot != last_hot_state) {
        last_hot_state = is_hot;
        if(is_hot) {
          Serial.println("[EVENT] Belief added: is_hot (true)");
          settings.get_event_base()->add_event(Event(EventOperator::BELIEF_ADDITION, Proposition(5)));
        } else {
          Serial.println("[EVENT] Belief deleted: is_hot (false)");
          settings.get_event_base()->add_event(Event(EventOperator::BELIEF_DELETION, Proposition(5)));
        }
      }

      bool is_humid = dht_humidity > 70.0;
      if (is_humid != last_humid_state) {
        last_humid_state = is_humid;
        if(is_humid) {
          Serial.println("[EVENT] Belief added: is_humid (true)");
          settings.get_event_base()->add_event(Event(EventOperator::BELIEF_ADDITION, Proposition(6)));
        } else {
          Serial.println("[EVENT] Belief deleted: is_humid (false)");
          settings.get_event_base()->add_event(Event(EventOperator::BELIEF_DELETION, Proposition(6)));
        }
      }
    } else {
      //Serial.println("[ERROR] Failed to read from DHT sensor!");
    }
  }

  /* IR Receiver reading (temporarily disabled)
  if (irrecv.decode(&results)) {
    Serial.printf("[SENSOR] IR code received: 0x%X\n", results.value);
    settings.get_event_base()->add_event(Event(EventOperator::BELIEF_ADDITION, Proposition(7)));
    // You could add plans here to react to specific codes
    irrecv.resume();
  }
  */

  // Network tasks
  if (current_time - last_discovery_time > DISCOVERY_INTERVAL_MS) {
    last_discovery_time = current_time;
    espnow_manager.send_discovery_broadcast();
  }
  if (current_time - last_cleanup_time > NEIGHBOR_TIMEOUT_MS) {
    last_cleanup_time = current_time;
    espnow_manager.cleanup_neighbors();
  }

  // Network belief synchronization
  if (current_time - last_belief_sync_time > 1000) {
      last_belief_sync_time = current_time;
      NeighborEntry_t neighbor;
      bool neighbor_found = espnow_manager.find_neighbor_by_capability(CAP_ACTUATOR_LED, &neighbor);

      if (neighbor_found && !has_neighbor_belief) {
          settings.get_event_base()->add_event(Event(EventOperator::BELIEF_ADDITION, Proposition(2)));
          settings.get_event_base()->add_event(Event(EventOperator::BELIEF_ADDITION, Proposition(3)));
          has_neighbor_belief = true;
      } else if (!neighbor_found && has_neighbor_belief) {
          settings.get_event_base()->add_event(Event(EventOperator::BELIEF_DELETION, Proposition(2)));
          settings.get_event_base()->add_event(Event(EventOperator::BELIEF_DELETION, Proposition(3)));
          has_neighbor_belief = false;
      }
  }

  // BDI cycle execution
  agent.run();
  
  // Print neighbor table
  if (current_time - last_print_time > 10000) {
    last_print_time = current_time;
    espnow_manager.print_neighbor_table();
  }

  delay(100);
}
