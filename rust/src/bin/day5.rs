use regex::Regex;
use std::{fs::File, io::Read};


fn get_data() -> String {
    let mut file = File::open("data/day5").unwrap();
    let mut content = String::new();
    file.read_to_string(&mut content).unwrap();
    content
}

fn part1() {
    let content = get_data();
    let re = Regex::new(r"(\d+),(\d+) -> (\d+),(\d+)").unwrap();
    for mt in re.captures_iter(&content) {
        // gross
        let mut allmatch = mt.iter();
        allmatch.next();
        let cap: Vec<u32> = allmatch
            .map(|x| x.unwrap().as_str().parse::<u32>().unwrap())
            .collect();
        println!("{:?}", cap);
    }
}

fn main() {
    part1();
}
