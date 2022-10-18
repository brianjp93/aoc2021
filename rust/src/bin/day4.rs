use std::{fs::File, io::Read};

type BoardType = Vec<Vec<u32>>;

#[derive(Debug, Clone)]
struct Board {
    board: BoardType,
    is_win: bool,
}

impl Board {
    fn from(board: BoardType) -> Board {
        return Board {
            board,
            is_win: false,
        }
    }
    fn is_win(&self, marked: &Vec<u32>) -> bool {
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
        false
    }
    fn score(&self, marked: &Vec<u32>, last: u32) -> u32 {
        let mut total = 0u32;
        for row in &self.board {
            for x in row {
                if !marked.contains(x) {
                    total += x;
                }
            }
        }
        return total * last
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

fn part1() -> Result<u32, ()> {
    let (nums, boards) = get_boards();
    let mut marked: Vec<u32> = Vec::new();
    for x in nums {
        marked.push(x.clone());
        for board in &boards {
            if board.is_win(&marked) {
                let score = board.score(&marked, x);
                return Ok(score)
            }
        }
    }
    Err(())
}

fn part2() -> Result<u32, ()>{
    let (nums, mut boards) = get_boards();
    let mut marked: Vec<u32> = Vec::new();
    for x in nums {
        marked.push(x.clone());
        for i in 0..boards.len(){
            if boards[i].is_win(&marked) {
                boards[i].is_win = true;
                if boards.iter().filter(|x| !x.is_win).collect::<Vec<&Board>>().len() == 0 {
                    return Ok(boards[i].score(&marked, x))
                }
            }
        }
    }
    Err(())
}

fn main() {
    let score1 = part1().unwrap();
    println!("part1: {:?}", score1);
    let score2 = part2().unwrap();
    println!("part1: {:?}", score2);
}
