use std::{fs::File, io::Read};

fn get_data() -> String {
    let mut file = File::open("data/day3").unwrap();
    let mut content = String::new();
    file.read_to_string(&mut content).unwrap();
    content
}

fn part1() -> u64 {
    let content = get_data();
    let mut line_count = 0;
    let mut vec_total: Vec<u32> = vec![0; 12];
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
    let output: Vec<f64> = vec_total
        .iter()
        .map(|x| {
            let out = *x as f64 / line_count as f64;
            let y = out.round();
            y
        })
        .collect();
    let mut gamma = 0u64;
    let mut eps = 0u64;
    for (i, n) in output.iter().rev().enumerate() {
        if n == &0f64 {
            gamma += 2u64.pow(i as u32);
        } else {
            eps += 2u64.pow(i as u32);
        }
    }
    gamma * eps
}

fn from_binary(binary: Vec<u32>) -> u32 {
    let mut dec = 0u32;
    for (i, n) in binary.iter().rev().enumerate() {
        dec += 2u32.pow(i as u32) * n;
    }
    dec
}

fn part2() -> u32 {
    let content = get_data();
    let mut data: Vec<Vec<u32>> = Vec::new();
    for line in content.lines() {
        let chars: Vec<u32> = line.chars().map(|x| x.to_digit(10u32).unwrap()).collect();
        data.push(chars);
    }
    let oxy = from_binary(filter_by_most_common(data.to_vec()));
    let co2 = from_binary(filter_by_least_common(data.to_vec()));
    oxy * co2
}

fn filter_by_most_common(mut data: Vec<Vec<u32>>) -> Vec<u32> {
    let mut bit = 0usize;
    while data.len() > 1 {
        let common = most_common(&data, bit);
        let mut new_data: Vec<Vec<u32>> = Vec::new();
        for line in data.iter() {
            if line[bit] == common {
                new_data.push(line.to_vec());
            }
        }
        data = new_data;
        bit += 1;
    }
    return data[0].to_vec();
}

fn filter_by_least_common(mut data: Vec<Vec<u32>>) -> Vec<u32> {
    let mut bit = 0usize;
    while data.len() > 1 {
        let common = least_common(&data, bit);
        let mut new_data: Vec<Vec<u32>> = Vec::new();
        for line in data.iter() {
            if line[bit] == common {
                new_data.push(line.to_vec());
            }
        }
        data = new_data;
        bit += 1;
    }
    return data[0].to_vec();
}

fn most_common(data: &Vec<Vec<u32>>, bit: usize) -> u32 {
    let mut one = 0;
    let mut zero = 0;
    for line in data.iter() {
        if line[bit] == 0 {
            zero += 1
        } else {
            one += 1
        }
    }
    if one > zero {
        return 1;
    } else if zero > one {
        return 0;
    } else {
        return 1;
    }
}

fn least_common(data: &Vec<Vec<u32>>, bit: usize) -> u32 {
    let mut one = 0;
    let mut zero = 0;
    for line in data.iter() {
        if line[bit] == 0 {
            zero += 1
        } else {
            one += 1
        }
    }
    if one > zero {
        return 0;
    } else if zero > one {
        return 1;
    } else {
        return 0;
    }
}

fn main() {
    let p1 = part1();
    println!("part 1: {}", p1);
    let p2 = part2();
    println!("part 2: {}", p2);
}
