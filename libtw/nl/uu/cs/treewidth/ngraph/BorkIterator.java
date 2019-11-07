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
import java.util.Iterator;

public class BorkIterator<E> implements Iterator<E> {

	ArrayList<E> src;
	boolean hasMore;
	int i;
	
	public BorkIterator( ArrayList<E> al ) {
		src = al;
		i = 0;
		hasMore = al.size()>0;
	}
	
	public boolean hasNext() {
		return hasMore;
	}

	public E next() {
		E ret = src.get( i );
		++i;
		hasMore = i < src.size();
		return ret;
	}

	public void remove() {
	}

}
