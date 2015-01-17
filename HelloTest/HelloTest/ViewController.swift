//
//  ViewController.swift
//  HelloTest
//
//  Created by Kevin Coxe on 1/16/15.
//  Copyright (c) 2015 Kevin Coxe. All rights reserved.
//

import UIKit

class Person {
    
    var name: [String:String]
    var list = [String:Int]()
    var location: String?
    
    init(firstName: String, lastName: String) {
        self.name = [firstName:lastName]
    }
}

class ViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }

    var people = [Person]()
    
    @IBOutlet weak var firstNameField: UITextField!
    @IBOutlet weak var lastNameField: UITextField!
    @IBAction func addPerson(sender: AnyObject) {
//        println("First name:\t\(firstNameField.text)")
//        println("Last name:\t\(lastNameField.text)")
        var newPerson = Person(firstName: firstNameField.text, lastName: lastNameField.text)
        people.append(newPerson)
        firstNameField.text = ""
        lastNameField.text = ""
    }
    
    @IBAction func showPeople(sender: AnyObject) {
        for person in people {
            println("Name:\t \(person.name)")
        }
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

