//
//  ViewController.swift
//  Pantry
//
//  Created by Kevin Coxe on 1/17/15.
//  Copyright (c) 2015 Randomly Generated. All rights reserved.
//

import UIKit



class ViewController: UIViewController, UITextFieldDelegate {

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }

    @IBOutlet weak var login_username: UITextField!
    @IBOutlet weak var login_password: UITextField!
    @IBAction func login_button(sender: AnyObject) {
        if login_username.text != nil && login_password.text != nil {
            println("username:\t \(login_username.text)")
            println("password:\t \(login_password.text)")
            
            login_username.text = ""
            login_password.text = ""
        } else {
            login_username.text = "Nope"
            login_password.text = "Nope"
        }
    }
    
    @IBAction func to_signin(sender: AnyObject) {
        let view2 = self.storyboard?.instantiateViewControllerWithIdentifier("view2") as myViewController2
        self.navigationController?.pushViewController(view2, animated: true)
    }
    
    func textFieldShouldReturn(textField: UITextField) -> Bool {
        textField.resignFirstResponder()
        return true
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

