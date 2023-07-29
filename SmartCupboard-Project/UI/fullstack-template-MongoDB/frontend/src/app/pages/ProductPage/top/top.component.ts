import { Component, OnInit,Input } from '@angular/core';

@Component({
  selector: 'ami-fullstack-top',
  templateUrl: './top.component.html',
  styleUrls: ['./top.component.scss']
})
export class TopComponent implements OnInit {

  @Input() PageProductName : any ;
  @Input()TotalNumItems : any ; 
  @Input() TotalWeight : any ; // Kg
  
  constructor() { }

  ngOnInit() {
  }
  
}