//
//  models.swift
//  Pantry
//
//  Created by Kevin Coxe on 1/17/15.
//  Copyright (c) 2015 Randomly Generated. All rights reserved.
//

import Foundation

class Person {
    
    var name: [String:String]
    var login: [String:String]
    var list = [String:Int]()
    var location: String?
    
    init(firstName: String, lastName: String, username: String, password: String) {
        self.name = [firstName:lastName]
        self.login = [username:password]
    }
}
