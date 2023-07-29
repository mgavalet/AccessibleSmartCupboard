import { Component, OnInit,Input } from '@angular/core';

@Component({
  selector: 'ami-fullstack-column-middle-two',
  templateUrl: './column-middle-two.component.html',
  styleUrls: ['./column-middle-two.component.scss']
})
export class ColumnMiddleTwoComponent implements OnInit {

  @Input() mariosData : any ; 

  constructor() { }

  ngOnInit() {
  }

}
