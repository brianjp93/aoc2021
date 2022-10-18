use std::{fs::File, io::Read};

type BoardType = Vec<Vec<u32>>;

#[derive(Debug)]
struct Board {
    board: BoardType,
}

impl Board {
    fn from(board: BoardType) -> Board {
        return Board {
            board,
        }
    }
    fn is_win(&mut self, marked: Vec<u32>) -> bool {
        let blen = self.board.len();
        for row in &self.board {
            if row.iter().filter(|x| marked.contains(x)).collect::<Vec<&u32>>().len() == blen {
                return true
            }
        }
        for x in 0..self.board[0].len() {
            let mut col: Vec<u32> = Vec::new();
            for y in 0..self.board.len() {
                col.push(self.board[y][x]);
            }
            if col.iter().filter(|x| marked.contains(x)).collect::<Vec<&u32>>().len() == blen {
                return true
            }
        }
        let mut dia: Vec<u32> = Vec::new();
        let mut dia2: Vec<u32> = Vec::new();
        for x in 0..4usize {
            dia.push(self.board[x][x]);
            dia2.push(self.board[blen-x-1][x])
        }
        if dia.iter().filter(|x| marked.contains(x)).collect::<Vec<&u32>>().len() == blen {
            return true
        }
        if dia2.iter().filter(|x| marked.contains(x)).collect::<Vec<&u32>>().len() == blen {
            return true
        }
        false
    }
}

fn get_data() -> String {
    let mut file = File::open("data/day4").unwrap();
    let mut content = String::new();
    file.read_to_string(&mut content).unwrap();
    content
}

fn get_boards() -> (Vec<u32>, Vec<Board>) {
    let mut boards: Vec<Board> = Vec::new();
    let content = get_data();
    let mut myiter = content.split("\n\n");
    let nums: Vec<u32> = myiter
        .next()
        .unwrap()
        .split(",")
        .map(|x| x.parse().unwrap())
        .collect();
    for mut part in myiter {
        part = part.trim();
        let board: BoardType = part
            .lines()
            .map(|line| {
                line.split_whitespace()
                    .map(|x| x.trim().parse::<u32>().unwrap())
                    .collect()
            })
            .collect();
        boards.push(Board::from(board));
    }
    return (nums, boards);
}

fn part1() {
    let (nums, boards) = get_boards();
    println!("nums: {:?}", nums);
    println!("boards: {:?}", boards);
}

fn main() {
    part1();
}
