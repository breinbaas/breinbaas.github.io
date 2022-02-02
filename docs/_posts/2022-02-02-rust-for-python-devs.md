---
layout: post
title:  "Rust - For Python devs"
date:   2022-02-02 18:48:49 +0200
categories: rust
---

### Rust for Python developers

Well the title is not completely correct because I also have a C++ background so things like stack and heap and memory management are not unknown to me but in this doc I simply notate all the things from the Rust book that are really different or powerful just as a reminder or lookup during Rust programming. Maybe it helps you too.

## A

### array loop 
```rust
let a: [10, 20, 30, 40]
for element in a.iter(){
    println!("The value is {}", element);  
}
```

## B

### break with result

```rust
let mut counter = 0;

let result = loop {
    counter += 1;
    if counter == 10{
        break counter; // will return counter as a result
    }
};

println!("The result is {}", result);
```

## E

### Enums

```rust
enum IpAddrKind{
    V4,
    V6,
}

let four = IpAddrKind::V4;

// with data
enum IpAddrKind{
    V4(String), // or V4(u8, u8, u8, u8)
    V6(String),
}

let four = IpAddrKind::V4(String::from(...));

match ip_address {
    IpAddrKind::V4 => ...
    ...
}

// with method
impl IpAddrKind {
    fb check(&self) -> bool{
        ...
    }
}

// option enum
enum Option<T>{
    Some(T),
    None,
};

let some = Some(5);
let some = Some("Hello World!");
let none: Option<u8> = None;

// samples
let x: i8 = 5;
let y: Option<i8> = Some(5);

let sum = x + y.unwrap_or(0); //unwrap will use the value or 0 if y = None

fn plus_one(x: Option<i32>) -> Option<i32> {
    match x {
        None => None,
        Some(i) => Some(i + 1),
    }
}
```

## F

### for loop over range
```rust
for number in 1..4 {
    println!("Number is {}", number)
}
```

## M

### matching default behaviour
```rust
match x {
    Some(i) -> ...,
    _ => None // default if not handled above
}
```



## N

### Null, None
See E - option enum

## S

### struct
```rust
struct User{
    name: String,
    email: String
}

// initialization
let user1 = User{
    email: String::from(...);
    name: String::from(...);
};

// initialization from other struct
let user2 = User {
    email: String::from(...);
    ..user1 // which will copy the other params from user1 and assign them to user2
};

// struct method
impl User{
    fn do_something(&self) -> u32 {
        //return something based on self
    }
    ...
}

// associated function (not tied to an instance of a struct)
impl User{
    fn do_something() -> User{
        User{
            ...
        }
    }
}
```

### print a struct
```rust
#[derive(Debug)]
struct BlaBla
...
println!("object: {:?}", object); // for non formatted output
println!("object: {:#?}", object); // for nicely formatted output
```

