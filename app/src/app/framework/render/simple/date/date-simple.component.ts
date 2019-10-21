/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 NETHINKS GmbH
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU Affero General Public License as
* published by the Free Software Foundation, either version 3 of the
* License, or (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU Affero General Public License for more details.

* You should have received a copy of the GNU Affero General Public License
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

import { Component, OnInit } from '@angular/core';
import { RenderField } from '../../fields/components.fields';
import { formatDate } from '@angular/common';

@Component({
  selector: 'cmdb-date-simple',
  templateUrl: './date-simple.component.html',
  styleUrls: ['./date-simple.component.scss']
})
export class DateSimpleComponent extends RenderField {

  constructor() {
    super();
  }

  public getSimpleDate(obj) {
    // ToDo: Recognize format by language
    if ( obj.day === undefined) {
      return 'TT.MM.JJJJ';
    }
    const format = 'dd/MM/yyyy';
    const myDate = obj.year + '-' + obj.month + '-' + obj.day;
    const locale = 'en-US';
    const formattedDate = formatDate(myDate, format, locale);
    return formattedDate;
  }
}
