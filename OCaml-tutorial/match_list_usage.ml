let rec f x l = 
    match l with
    | [] -> 1
    | h :: hs -> if h = x then 1
                else 1 + f x hs
