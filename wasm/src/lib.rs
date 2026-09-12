use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn fuzzy_match(input: &str, target: &str) -> bool {
    let a = input.to_lowercase();
    let b = target.to_lowercase();
    if a.contains(&b) || b.contains(&a) { return true; }
    levenshtein(&a, &b) <= 2
}

#[wasm_bindgen]
pub fn is_valid_command(input: &str) -> bool {
    let cmds = ["jump","fall","crouch","lie","stand","spin","invis","creeper","day","night","achievements"];
    let s = input.trim().to_lowercase();
    for c in cmds { if fuzzy_match(&s, c) { return true; } }
    false
}

#[wasm_bindgen]
pub fn process_skin_pixels(data: Vec<u8>) -> Vec<u8> {
    let mut out = data.clone();
    for i in (0..out.len()).step_by(4) {
        if out[i+3] > 0 {
            out[i] = out[i].wrapping_add(1);
        }
    }
    out
}

#[wasm_bindgen]
pub fn wasm_version() -> String { "steve-wasm v1.0.0".to_string() }

#[wasm_bindgen]
pub fn achievements_progress(counts: Vec<u8>) -> u8 {
    counts.iter().filter(|&&x| x != 0).count() as u8
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
