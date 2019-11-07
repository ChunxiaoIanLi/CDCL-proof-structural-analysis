/*
 * Copyright (C) 2006 
 * Thomas van Dijk
 * Jan-Pieter van den Heuvel
 * Wouter Slob
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
 */
 
package nl.uu.cs.treewidth.ngraph;

import java.util.ArrayList;

public class NVertexOrder< D > {
	
	public NVertexOrder() {
		order = new ArrayList<NVertex<D>>();
	}
	public NVertexOrder( int size ) {
		order = new ArrayList<NVertex<D>>( size );
	}
	public NVertexOrder( NVertexOrder<D> other ) {
		order = new ArrayList<NVertex<D>>( other.order );
	}
	
	public ArrayList<NVertex<D>> order;
	
	public String toString() {
		String s = "";
		for( NVertex<D> v : order) {
			s = s.concat( " " + v.data.toString() );
		}
		return s;
	}
}
