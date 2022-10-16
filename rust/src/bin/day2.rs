use std::{fs::File, io::Read};
use regex::Regex;


fn get_data() -> String {
    let mut file = File::open("data/day2").unwrap();
    let mut content = String::new();
    file.read_to_string(&mut content).unwrap();
    content
}

fn part1() -> i64 {
    let mut position = 0;
    let mut depth = 0;
    let data = get_data();
    let re = Regex::new(r"(\w+)\s(\d+)").unwrap();
    for mt in re.captures_iter(&data) {
        let direction =  mt.get(1).map_or("", |m| m.as_str());
        let n = mt.get(2).map_or("", |m| m.as_str()).parse::<i16>().unwrap();
        match direction {
            "forward" => {position += n}
            "up" => {depth -= n}
            "down" => {depth += n}
            _ => panic!("?")
        }
    }
    return (position as i64) * (depth as i64);
}

fn part2() -> i64 {
    let mut aim: i64 = 0;
    let mut position: i64 = 0;
    let mut depth: i64 = 0;
    let data = get_data();
    let re = Regex::new(r"(\w+)\s(\d+)").unwrap();
    for mt in re.captures_iter(&data) {
        let direction =  mt.get(1).map_or("", |m| m.as_str());
        let n = mt.get(2).map_or("", |m| m.as_str()).parse::<i64>().unwrap();
        match direction {
            "up" => {aim -= n}
            "down" => {aim += n}
            "forward" => {
                position += n;
                depth += n * aim
            }
            _ => panic!("?")
        }
    }
    return position * depth;
}

fn main() {
    let part1 = part1();
    let part2 = part2();
    println!("part1: {}", part1);
    println!("part2: {}", part2);
}
