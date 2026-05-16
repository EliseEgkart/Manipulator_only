#include <Arduino.h>

String rx_line = "";

float joint_deg[4] = {0.0, 0.0, 0.0, 0.0};
unsigned long last_cmd_time = 0;

// =========================================================
// Function prototypes
// =========================================================
void readSerialCommand();
void handleCommand(const String &cmd);
void parseCmdPos(const String &cmd);
int splitCsv(const String &line, String *out, int max_parts);

void setup()
{
  Serial.begin(115200);

  while (!Serial)
  {
    delay(10);
  }

  delay(1000);
  Serial.println("READY");
}

void loop()
{
  readSerialCommand();

  // 10Hz 상태 송신
  static unsigned long last_state_time = 0;

  if (millis() - last_state_time >= 100)
  {
    last_state_time = millis();

    Serial.print("STATE,");
    Serial.print(millis());
    Serial.print(",");
    Serial.print(joint_deg[0], 3);
    Serial.print(",");
    Serial.print(joint_deg[1], 3);
    Serial.print(",");
    Serial.print(joint_deg[2], 3);
    Serial.print(",");
    Serial.print(joint_deg[3], 3);
    Serial.println(",OK");
  }
}

void readSerialCommand()
{
  while (Serial.available() > 0)
  {
    char c = Serial.read();

    if (c == '\n')
    {
      rx_line.trim();

      if (rx_line.length() > 0)
      {
        handleCommand(rx_line);
      }

      rx_line = "";
    }
    else
    {
      rx_line += c;
    }
  }
}

void handleCommand(const String &cmd)
{
  if (cmd == "PING")
  {
    Serial.println("PONG");
    return;
  }

  if (cmd == "STOP")
  {
    Serial.println("ACK_STOP");
    return;
  }

  if (cmd.startsWith("CMD_POS"))
  {
    parseCmdPos(cmd);
    return;
  }

  Serial.print("ERR,UNKNOWN,");
  Serial.println(cmd);
}

void parseCmdPos(const String &cmd)
{
  // Expected:
  // CMD_POS,seq,j1_deg,j2_deg,j3_deg,j4_deg

  String parts[6];
  int part_count = splitCsv(cmd, parts, 6);

  if (part_count < 6)
  {
    Serial.println("ERR,CMD_POS_FORMAT");
    return;
  }

  String seq = parts[1];

  joint_deg[0] = parts[2].toFloat();
  joint_deg[1] = parts[3].toFloat();
  joint_deg[2] = parts[4].toFloat();
  joint_deg[3] = parts[5].toFloat();

  last_cmd_time = millis();

  Serial.print("ACK,");
  Serial.println(seq);
}

int splitCsv(const String &line, String *out, int max_parts)
{
  int count = 0;
  int start = 0;

  while (count < max_parts)
  {
    int comma = line.indexOf(',', start);

    if (comma == -1)
    {
      out[count++] = line.substring(start);
      break;
    }

    out[count++] = line.substring(start, comma);
    start = comma + 1;
  }

  return count;
}