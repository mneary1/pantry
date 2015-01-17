//
//  myViewController2.swift
//  Pantry
//
//  Created by Kevin Coxe on 1/17/15.
//  Copyright (c) 2015 Randomly Generated. All rights reserved.
//

import UIKit

class myViewController2: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }

    @IBOutlet weak var signup_firstName: UITextField!
    @IBOutlet weak var signup_lastName: UITextField!
    @IBOutlet weak var signup_username: UITextField!
    @IBOutlet weak var signup_pass: UITextField!
    @IBOutlet weak var signup_pass_confirm: UITextField!
    
    var people = [Person]()
    
    @IBAction func save_signup(sender: AnyObject) {
        
        if signup_pass == signup_pass_confirm {
            var new_person = Person(firstName: signup_firstName.text, lastName: signup_lastName.text, username: signup_username.text, password: signup_pass.text)
            people.append(new_person)
            self.navigationController?.popToRootViewControllerAnimated(true)
        } else {
            signup_pass.text = ""
            signup_pass_confirm.text = ""
        }
        
        
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
