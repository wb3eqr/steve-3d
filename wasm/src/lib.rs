use wasm_bindgen::prelude::*;
use base64::{Engine as _, engine::general_purpose};

const SECRET: &[u8] = b"steve_wasm_secret_2025_90_XOR";
const PROOF_TTL_MS: f64 = 5000.0;

fn all_aliases() -> Vec<(&'static str, Vec<&'static str>)> {
 vec![
  ("spin", vec!["╨║╤А╤Г╤В╨░╨╜╨╕╤Б╤М", "╨║╤А╤Г╤В╨╕╤Б╤М", "╨║╤А╤Г╤В╨╜╨╕╤Б╤М", "╨┐╨╛╨║╤А╤Г╤В╨╕╤Б╤М", "╨▓╨╡╤А╤В╨░╨╜╨╕╤Б╤М", "╨║╤А╤Г╤В╨░╨╜╤Г╤В╤М"]),
  ("salto", vec!["╤Б╨░╨╗╤М╤В╨╛", "╤Б╨░╨╗╤М╤В╤Г╤Е╨░", "╨║╤Г╨▓╤Л╤А╨╛╨║", "╤Д╨╗╨╕╨┐", "╨┐╨╡╤А╨╡╨▓╨╛╤А╨╛╤В", "╤Б╨░╨╗╤М╤В╨░╨╜╤Г╤В╤М"]),
  ("hit", vec!["╤Г╨┤╨░╤А", "╤Г╨┤╨░╤А╤М", "╨▒╨╡╨╣", "╨░╤В╨░╨║╨░", "╤Е╨╕╤В", "╤Б╤В╤Г╨║╨╜╨╕"]),
  ("invis", vec!["╨╜╨╡╨▓╨╕╨┤╨╕╨╝╨╛╤Б╤В╤М", "╨╜╨╡╨▓╨╕╨┤╨╕╨╝╨║╨░", "╨╕╤Б╤З╨╡╨╖╨╜╨╕", "╤Б╨┐╤А╤П╤З╤М╤Б╤П", "╨╕╨╜╨▓╨╕╨╖", "╤Б╨║╤А╤Л╤В╤М╤Б╤П"]),
  ("crouch", vec!["╨┐╤А╨╕╤Б╨╡╤Б╤В╤М", "╨┐╤А╨╕╤Б╤П╨┤╤М", "╤Б╨╕╨┤╨╡╤В╤М", "╨┐╤А╨╕╨│╨╜╨╕╤Б╤М", "╨║╤А╨░╤Г╤З", "╨╜╨░ ╨║╨╛╤А╤В╨╛╤З╨║╨╕"]),
  ("jump", vec!["╨┐╤А╤Л╨│╨╜╤Г╤В╤М", "╨┐╤А╤Л╨╢╨╛╨║", "╨┐╤А╤Л╨│╨╜╨╕", "╨┤╨╢╨░╨╝╨┐", "╨┐╤А╤Л╨│╨░╨╣", "╨┐╨╛╨┤╨┐╤А╤Л╨│╨╜╨╕"]),
  ("creeper", vec!["╨║╤А╨╕╨┐╨╡╤А", "╨║╤А╨╕╨┐╨╡╤А╨╛╨╝", "╤Б╤В╨░╨╜╤М ╨║╤А╨╕╨┐╨╡╤А╨╛╨╝", "╨║╤А╨╡╨┐╨┐╨╡╤А", "creeper", "╨┐╤А╨╡╨▓╤А╨░╤В╨╕╤Б╤М ╨▓ ╨║╤А╨╕╨┐╨╡╤А╨░"]),
  ("fall", vec!["╤Г╨┐╨░╨╗", "╤Г╨┐╨░╤Б╤В╤М", "╨┐╨░╨┤╨░╤В╤М", "╨┐╨░╨┤╨╡╨╜╨╕╨╡", "╤Б╨▓╨░╨╗╨╕╨╗╤Б╤П", "╨│╤А╨╛╤Е╨╜╤Г╨╗╤Б╤П", "╨┐╨╛╨▓╨░╨╗╨╕╨╗╤Б╤П", "╤Г╤А╨╛╨╜╨╕╨╗╤Б╤П", "╤Г╨┐╨░╨┤╨╕", "╨┐╨░╨┤╨╕"]),
  ("block", vec!["╨▒╨╗╨╛╨║", "╨┐╨╛╤Б╤В╨░╨▓╤М ╨▒╨╗╨╛╨║", "╨┤╨╡╤А╨╜", "╨┐╨╛╤Б╤В╨░╨▓╨╕╤В╤М ╨▒╨╗╨╛╨║", "╨▒╨╗╨╛╨║ ╨┤╨╡╤А╨╜╨░", "╨┐╨╛╤Б╤В╨░╨▓╤М ╨┤╨╡╤А╨╜", "╨┐╨╛╤Б╤В╨░╨▓╨╕╤В╤М ╨┤╨╡╤А╨╜", "╨▒╨╗╨╛╨║ ╨╖╨╡╨╝╨╗╨╕"]),
  ("dance", vec!["╤В╨░╨╜╨╡╤Ж", "╤В╨░╨╜╤Ж╤Г╨╣", "╤В╨░╨╜╤Ж╨╡╨▓╨░╤В╤М", "╨┤╨╡╨╜╤Б", "dance", "╤В╨░╨╜╤Ж╤Л", "╨┐╨╗╤П╤И╨╕", "╨┐╨╗╤П╤Б", "╤В╨░╨╜╤Ж╤Г╨╣ ╤В╨░╨╜╨╡╤Ж"]),
  ("crash", vec!["╨║╤А╨░╤И", "╤Б╨╗╨╛╨╝╨░╨╣╤Б╤П", "╤А╨░╨╖╨╗╨╛╨╝╨░╨╣╤Б╤П", "╨┐╨╛╨╗╨╛╨╝╨║╨░", "crash", "╤Б╨╗╨╛╨╝╨░╨╣", "╤А╨░╨╖╨▓╨░╨╗╨╕╤В╤М╤Б╤П", "╨║╤А╨░╤И╨╜╨╕"]),
  ("run", vec!["╨▒╨╡╨│╨╕", "╨▒╨╡╨╢╨░╤В╤М", "╨┐╨╛╨▒╨╡╨│╨╕", "╨▒╨╡╨│", "run", "╨▒╨╡╨│╨╛╨╝", "╨╝╤З╨╕", "╨╜╨╡╤Б╨╕╤Б╤М"]),
  ("fly", vec!["╨┐╨╛╨╗╨╡╤В", "╨╗╨╡╤В╨╕", "╨▓╨╖╨╗╨╡╤В╨╕", "╨┐╨╛╨╗╨╡╤В╨╡╤В╤М", "fly", "╨▓╨╖╨╝╤Л╤В╤М", "╨┐╨░╤А╨╡╨╜╨╕╨╡"]),
  ("shake", vec!["╨┤╤А╨╛╨╢╤М", "╤В╤А╤П╤Б╨╕╤Б╤М", "╨┤╤А╨╛╨╢╨╕", "╤В╤А╤П╤Б╨║╨░", "shiver", "╨▓╨╕╨▒╤А╨░╤Ж╨╕╤П"]),
  ("zombie", vec!["╨╖╨╛╨╝╨▒╨╕", "╤Б╤В╨░╨╜╤М ╨╖╨╛╨╝╨▒╨╕", "╨╖╨╛╨╝╨▒╨╕ ╨╝╨╛╤А╤Д", "╨╖╨╛╨╝╨▒╨░╨║", "╨╖╨╛╨╝╨▒╨╕╨║"]),
  ("giant", vec!["╨│╨╕╨│╨░╨╜╤В", "╨▒╨╛╨╗╤М╤И╨╛╨╣", "╨▓╤Л╤А╨░╤Б╤В╨╕", "╤Г╨▓╨╡╨╗╨╕╤З╤М╤Б╤П", "╨│╨╕╨│╨░╨╜╤В╨╕╨╖╨╝", "╨▓╨╡╨╗╨╕╨║╨░╨╜"]),
  ("tiny", vec!["╨╝╨╡╨╗╨║╨╕╨╣", "╨║╤А╨╛╤И╨║╨░", "╤Г╨╝╨╡╨╜╤М╤И╨╕╤Б╤М", "╨╝╨░╨╗╨╡╨╜╤М╨║╨╕╨╣", "╨║╨░╤А╨╗╨╕╨║", "tiny"]),
  ("rainbow", vec!["╤А╨░╨┤╤Г╨│╨░", "╤А╨░╨┤╤Г╨╢╨╜╤Л╨╣", "╤Ж╨▓╨╡╤В╨╜╨╛╨╣", "╤Б╨┐╨╡╨║╤В╤А", "rainbow", "╨┐╨╡╤А╨╡╨╗╨╕╨▓╨░╨╣╤Б╤П"]),
  ("ghost", vec!["╨┐╤А╨╕╨╖╤А╨░╨║", "╨┐╤А╨╕╨▓╨╕╨┤╨╡╨╜╨╕╨╡", "╤Д╨░╨╜╤В╨╛╨╝", "╨┤╤Г╤Е", "ghost", "╨┐╤А╨╕╨╖╤А╨░╤З╨╜╤Л╨╣"]),
  ("wave", vec!["╨▓╨╛╨╗╨╜╨░", "╨╝╨░╤И╨╕", "╨┐╨╛╨╝╨░╤И╨╕", "╨┐╤А╨╕╨▓╨╡╤В", "wave", "╨╝╨░╤Е╨░╨╜╨╕╨╡"]),
  ("storm", vec!["╨▒╤Г╤А╤П", "╨▓╨╕╤Е╤А╤М", "╤Г╤А╨░╨│╨░╨╜", "╤Б╨╝╨╡╤А╤З", "storm", "╤В╨╛╤А╨╜╨░╨┤╨╛"]),
  ("teleport", vec!["╤В╨╡╨╗╨╡╨┐╨╛╤А╤В", "╤В╨┐", "╨┐╨╡╤А╨╡╨╝╨╡╤Б╤В╨╕╤Б╤М", "warp", "teleport"]),
  ("clone", vec!["╨║╨╗╨╛╨╜", "╨║╨╗╨╛╨╜╨╕╤А╤Г╨╣", "╨┤╤Г╨▒╨╗╤М", "clone", "╨┤╨▓╨╛╨╣╨╜╨╕╨║"]),
  ("fire", vec!["╨╛╨│╨╛╨╜╤М", "╨│╨╛╤А╨╕", "╨┐╨╗╨░╨╝╤П", "fire", "╨▓╨╛╤Б╨┐╨╗╨░╨╝╨╡╨╜╨╕╤Б╤М"]),
  ("water", vec!["╨▓╨╛╨┤╨░", "╨▓╨╛╨┤╨╜╤Л╨╣", "╨▒╤Г╨╗╤М╨║", "water", "╨╜╨░╨╝╨╛╤З╨╕╤Б╤М"]),
  ("ice", vec!["╨╗╨╡╨┤", "╨╗╤С╨┤", "╨╖╨░╨╝╨╡╤А╨╖╨╜╨╕", "ice", "╨╝╨╛╤А╨╛╨╖"]),
  ("lightning", vec!["╨╝╨╛╨╗╨╜╨╕╤П", "╨│╤А╨╛╨╝", "╤А╨░╨╖╤А╤П╨┤", "lightning", "╨╝╨╛╨╗╨╜╨╕╨╡╨╣"]),
  ("explosion", vec!["╨▓╨╖╤А╤Л╨▓", "╨▒╨░╤Е", "╨▒╤Г╨╝", "explosion", "╨▓╨╖╨╛╤А╨▓╨╕╤Б╤М"]),
  ("void", vec!["╨┐╤А╨╛╨▓╨░╨╗", "╨▒╨╡╨╖╨┤╨╜╨░", "╨┐╨░╨┤╨╕ ╨▓ ╨▒╨╡╨╖╨┤╨╜╤Г", "void", "╨┐╤А╨╛╨┐╨░╤Б╤В╤М"]),
  ("parkour", vec!["╨┐╨░╤А╨║╤Г╤А", "╨┐╤А╤Л╨│╨░╨╣ ╨┐╨░╤А╨║╤Г╤А", "parkour", "╤Б╨║╨░╤З╨╛╨║"]),
  ("disco", vec!["╨┤╨╕╤Б╨║╨╛", "╨┤╨╕╤Б╨║╨╛╤В╨╡╨║╨░", "╨▓╨╡╤З╨╡╤А╨╕╨╜╨║╨░", "disco", "╤В╤Г╤Б╨░"]),
  ("robot", vec!["╤А╨╛╨▒╨╛╤В", "╨╝╨╡╤Е╨░╨╜╨╕╨╖╨╝", "╨║╨╕╨▒╨╛╤А╨│", "robot", "╨╢╨╡╨╗╨╡╨╖╤П╨║╨░"]),
  ("ninja", vec!["╨╜╨╕╨╜╨┤╨╖╤П", "╤Б╨║╤А╤Л╤В╨╜╨╛╤Б╤В╤М", "╤В╨╡╨╜╤М", "ninja", "╤И╨╕╨╜╨╛╨▒╨╕"]),
  ("space", vec!["╨║╨╛╤Б╨╝╨╛╤Б", "╨╜╨╡╨▓╨╡╤Б╨╛╨╝╨╛╤Б╤В╤М", "╨╛╤А╨▒╨╕╤В╨░", "space", "╨│╨░╨╗╨░╨║╤В╨╕╨║╨░"]),
  ("gravity", vec!["╨│╤А╨░╨▓╨╕╤В╨░╤Ж╨╕╤П", "╤В╤П╨╢╨╡╤Б╤В╤М", "╨┐╤А╨╕╤В╤П╨╢╨╡╨╜╨╕╨╡", "gravity", "╨░╨╜╤В╨╕╨│╤А╨░╨▓"]),
  ("magnet", vec!["╨╝╨░╨│╨╜╨╕╤В", "╨┐╤А╨╕╤В╤П╨╜╨╕", "╨╝╨░╨│╨╜╨╡╤В╨╕╨╖╨╝", "magnet", "╨┐╤А╨╕╨╝╨░╨│╨╜╨╕╤В╤М"]),
  ("summon", vec!["╨┐╤А╨╕╨╖╤Л╨▓", "╨┐╤А╨╕╨╖╨╛╨▓╨╕", "╨▓╤Л╨╖╨╛╨▓╨╕", "summon", "╨┐╨╕╤В╨╛╨╝╨╡╤Ж"]),
  ("time", vec!["╨▓╤А╨╡╨╝╤П", "╨┤╨╡╨╜╤М", "╨╜╨╛╤З╤М", "time", "╤Б╨╝╨╡╨╜╨░ ╨▓╤А╨╡╨╝╨╡╨╜╨╕"]),
  ("shield", vec!["╤Й╨╕╤В", "╨╖╨░╤Й╨╕╤В╨░", "╤Й╨╕╤В ╨▒╨╗╨╛╨║", "shield"]),
  ("bow", vec!["╨╗╤Г╨║", "╤Б╤В╤А╨╡╨╗╤М╨▒╨░", "╨▓╤Л╤Б╤В╤А╨╡╨╗", "bow"]),
  ("elytra", vec!["╤Н╨╗╨╕╤В╤А╨░", "╨║╤А╤Л╨╗╤М╤П", "elytra", "╨┐╨╗╨░╨╜╨╕╤А╨╛╨▓╨░╨╜╨╕╨╡"]),
  ("totem", vec!["╤В╨╛╤В╨╡╨╝", "╨▒╨╡╤Б╤Б╨╝╨╡╤А╤В╨╕╨╡", "totem"]),
  ("dragon", vec!["╨┤╤А╨░╨║╨╛╨╜", "╨┤╤А╨░╨║╨╛╨╜╨╕╨╣", "dragon"]),
  ("portal", vec!["╨┐╨╛╤А╤В╨░╨╗", "╤Н╨╜╨┤", "╨┐╨╛╤А╤В╨░╨╗ ╨▓ ╤Н╨╜╨┤", "portal"]),
  ("chameleon", vec!["╤Е╨░╨╝╨╡╨╗╨╡╨╛╨╜", "╨╝╨░╤Б╨║╨╕╤А╨╛╨▓╨║╨░", "chameleon"]),
  ("wind", vec!["╨▓╨╡╤В╨╡╤А", "wind", "╨▓╨╕╤Е╤А╤М ╨▓╨╡╤В╤А╨░"]),
  ("lava", vec!["╨╗╨░╨▓╨░", "lava", "╨╗╨░╨▓╨░ ╨║╨╕╨┐╨╡╨╜╨╕╨╡"]),
  ("snow", vec!["╤Б╨╜╨╡╨│", "╤Б╨╜╨╡╨│╨╛╨┐╨░╨┤", "snow", "╤Б╤Г╨│╤А╨╛╨▒"]),
  ("reset", vec!["╤Б╨▒╤А╨╛╤Б", "╤Б╨▒╤А╨╛╤Б╨╕╤В╤М", "╤Б╨▒╤А╨╛╤Б ╨░╤З╨╕╨▓╨╛╨║", "╨╛╤З╨╕╤Б╤В╨╕╤В╤М", "╨╛╤З╨╕╤Б╤В╨╕╤В╤М ╨░╤З╨╕╨▓╨║╨╕", "reset", "clear", "╤Б╨▒╤А╨╛╤Б ╨┐╤А╨╛╨│╤А╨╡╤Б╤Б╨░"]),
 ]
}

fn normalize(s: &str) -> String {
  let mut t = s.to_lowercase().trim().to_string();
  t = t.replace("ё", "е");
  t = t.chars().filter(|c| !matches!(c, '!' | '?' | '.' | ',' )).collect();
  t.split_whitespace().collect::<Vec<_>>().join(" ")
}

fn levenshtein(a: &str, b: &str) -> usize {
  let a: Vec<char> = a.chars().collect();
  let b: Vec<char> = b.chars().collect();
  let mut dp = vec![vec![0; b.len()+1]; a.len()+1];
  for i in 0..=a.len() { dp[i][0]=i; }
  for j in 0..=b.len() { dp[0][j]=j; }
  for i in 1..=a.len() {
    for j in 1..=b.len() {
      let cost = if a[i-1]==b[j-1] {0} else {1};
      dp[i][j] = (dp[i-1][j]+1).min(dp[i][j-1]+1).min(dp[i-1][j-1]+cost);
    }
  }
  dp[a.len()][b.len()]
}

fn matches_aliases(input: &str, aliases: &[&str]) -> bool {
  let norm = normalize(input);
  if norm.is_empty() { return false; }
  for a in aliases {
    let a_norm = normalize(a);
    if norm == a_norm { return true; }
    if norm.contains(&a_norm) && (norm.len() as i32 - a_norm.len() as i32).abs() <= 1 { return true; }
    if a_norm.len()<=3 || norm.len()<=3 {
      let a2 = a_norm.trim_end_matches("сь");
      let n2 = norm.trim_end_matches("сь");
      if a2==n2 { return true; }
      continue;
    }
    if a_norm.chars().next() != norm.chars().next() { continue; }
    let min_len = norm.len().min(a_norm.len());
    let max_dist = if min_len <=4 {0} else if min_len <=6 {1} else {2};
    if levenshtein(&norm, &a_norm) <= max_dist && (norm.len() as i32 - a_norm.len() as i32).abs() <=1 { return true; }
    let a2 = a_norm.trim_end_matches("сь");
    let n2 = norm.trim_end_matches("сь");
    if a2==n2 { return true; }
    if n2.len()>=7 && a2.chars().next()==n2.chars().next() && levenshtein(n2,a2)<=1 && (n2.len() as i32 - a2.len() as i32).abs()<=1 { return true; }
  }
  false
}

#[wasm_bindgen]
pub fn fuzzy_match(input: &str, target: &str) -> bool {
  matches_aliases(input, &[target])
}

#[wasm_bindgen]
pub fn is_valid_command(input: &str) -> bool {
  !check_command(input).is_empty()
}

#[wasm_bindgen]
pub fn check_command(input: &str) -> String {
  let norm = normalize(input);
  if norm.is_empty() { return String::new(); }
  for (cmd, aliases) in all_aliases() {
    if matches_aliases(input, &aliases) { return cmd.to_string(); }
  }
  String::new()
}

fn simple_hash(data: &[u8]) -> u64 {
  let mut h: u64 = 1469598103934665603;
  for &b in data {
    h ^= b as u64;
    h = h.wrapping_mul(1099511628211);
    h ^= SECRET[(h as usize) % SECRET.len()] as u64;
  }
  h
}

#[wasm_bindgen]
pub fn generate_proof(command: &str, ts: f64) -> String {
  let mut data = Vec::new();
  data.extend_from_slice(command.as_bytes());
  data.extend_from_slice(&ts.to_le_bytes());
  data.extend_from_slice(SECRET);
  let h = simple_hash(&data);
  let mut bytes = Vec::new();
  bytes.extend_from_slice(&h.to_le_bytes());
  bytes.extend_from_slice(&(ts as u64).to_le_bytes());
  general_purpose::STANDARD.encode(&bytes)
}

#[wasm_bindgen]
pub fn verify_proof(command: &str, token: &str, now_ms: f64) -> bool {
  let decoded = match general_purpose::STANDARD.decode(token) {
    Ok(v) => v, Err(_) => return false,
  };
  if decoded.len() < 16 { return false; }
  let mut h_bytes = [0u8;8];
  h_bytes.copy_from_slice(&decoded[0..8]);
  let mut ts_bytes = [0u8;8];
  ts_bytes.copy_from_slice(&decoded[8..16]);
  let ts = u64::from_le_bytes(ts_bytes) as f64;
  if (now_ms - ts).abs() > PROOF_TTL_MS { return false; }
  if now_ms < ts { return false; }
  let expected = generate_proof(command, ts);
  expected == token
}

#[wasm_bindgen]
pub fn process_skin_pixels(data: Vec<u8>) -> Vec<u8> {
  let mut out = data.clone();
  for i in (0..out.len()).step_by(4) {
    if out[i+3] > 0 { out[i] = out[i].wrapping_add(1); }
  }
  out
}

#[wasm_bindgen]
pub fn wasm_version() -> String { "steve-wasm v2.0-secure".to_string() }

#[wasm_bindgen]
pub fn achievements_progress(counts: Vec<u8>) -> u8 {
  counts.iter().filter(|&&x| x != 0).count() as u8
}
