(* Here is the tutorial code in class 2018/2/7 *)

(* simple usages *)
let f x = x + 1
let id x = x
let f = fun x -> x + 1

(* partial application *)
let add = fun x -> fun y -> x + y

(* sub-function define *)
let g x = 
    let y = f x in
    y + y

let g1 x =
    f x + f x

let g2 x =
    let y = f x and z = f x in
    y + z

(* recursion *)
let rec fact n = 
    if n <= 0 then 1
    else n * fact (n - 1)

let rec fact1 n =
    let r = n * fact (n - 1) in 
        if n <= 0 then 1
        else r

(* pairs *)
let addPair p = 
    let (p1, p2) = p in
        p1 + p2     (* + for int *)

let addPair2 p = 
    let (p1, p2, p3) = p in
        p1 ^ p2 ^ p3(* ^ for string *)

(* list *)
let l1 = [1; 2; 4]
let l2 = 1 :: 3 :: 4 :: []
let l3 = l1 @ l2    (* @ is list concat op *)

let rec sumList l = 
    match l with
    | [] -> 0   (* [] means the type is 'list' *)
    | x :: xs -> x + sumList xs

let rec drop x l = 
    match l with 
    | [] -> []
    | y :: ys -> if x = (*1*) y then drop x ys
                else y :: drop x ys
(*1 In OCaml syntax, =  <> means equality/inequality (deep)
 *              and == != means equality/inequality (shallow)
 *  We basically should always be using = to compare any kind of values. 
 *  <https://stackoverflow.com/questions/13590307/whats-the-difference-between-equal-and-identical-in-ocaml> *)

(* iter, map, reduce *)
let printIter l = 
    List.iter (Printf.printf "%s: ") l

let incList l =
    List.map (fun x -> x + 1) l

let int2string l = 
    List.map (fun x -> string_of_int x) l

let foldSum l =
    List.fold_left (+) 0 l

let rec map f l =
    match l with
    | [] -> []
    | x :: xs -> f x :: map f xs

type color =
    | Green
    | Blue
    | Red

let cstr c =
    match c with
    | Green -> "Green"
    | Blue -> "Blue"
    | Red -> "Red"

type colorInt =
    | Green of int
    | Blue of int
    | Red of int

let cstr c =
    match c with
    | Green x -> "Green" ^ string_of_int x
    | Blue x -> "Blue" ^ string_of_int x
    | Red x -> "Red" ^ string_of_int x

type ourlist = 
    | Empty
    | Cons of int * ourlist

let rec sumList l =
    match l with 
    | Empty -> 0
    | Cons (x, xs) -> x + sumList xs

type expr = 
    | Num of int
    | Plus of (expr * expr)
    | Times of (expr * expr)

let rec eval e =
    match e with 
    | Num x -> x
    | Plus (e1, e2) -> eval e1 + eval e2
    | Times (e1, e2) -> eval e1 * eval e2

    
