use std::{fs::File, io::Read};

fn get_data() -> String {
    let mut file = File::open("data/day3").unwrap();
    let mut content = String::new();
    file.read_to_string(&mut content).unwrap();
    content
}

fn main() {
    let content = get_data();
    let mut line_count = 0;
    let mut vec_total: Vec<u32> = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0].into_iter().collect();
    for line in content.lines() {
        line_count += 1;
        let chars: Vec<u32> = line
            .chars()
            .map(|x| x.to_digit(10 as u32).unwrap())
            .collect();
        for (i, n) in chars.iter().enumerate() {
            vec_total[i] += n
        }
    }
    let output: Vec<f64> = vec_total.iter().map(|x| {
        let out = *x as f64 / line_count as f64;
        let y = out.round();
        y
    }).collect();
    let mut gamma = 0u64;
    let mut eps = 0u64;
    println!("{:?}", output);
    for (i, n) in output.iter().rev().enumerate() {
        println!("{}, {}", i, n);
        if n == &0f64 {
            gamma += i.pow(2) as u64;
        } else {
            eps += i.pow(2) as u64;
        }
    }
    let power = gamma * eps;
    println!("{:?}", power);
}
