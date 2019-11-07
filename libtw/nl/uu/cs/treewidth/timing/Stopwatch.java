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
 
package nl.uu.cs.treewidth.timing;

/**
 * <p>A stopwatch can be used to measure intervals.</p>
 * 
 * <p>
 * <i>Example usage:</i> Simple timing.
 * </p>
 * <pre>
 * Stopwatch t = new Stopwatch();
 * 
 * t.start();
 *  ... do something ...
 * t.stop();
 * 
 * long millisecondsPassed = t.getTime(); 
 * </pre>
 * 
 * 
 * 
 * <p>
 * <i>Example usage:</i> repeat something until a second has passed. (Note
 * that this only checks the time once every iteration, so it `do something'
 * is expensive you can significantly overshoot one second.)
 * </p>
 * <pre>
 * Stopwatch t = new Stopwatch();
 * 
 * t.start();
 * while( t.getTime() < 1000 ) {
 *     ... do something ...
 * }
 * t.stop();
 * </pre>
 * 
 * 
 * 
 * <p>
 * <i>Example usage:</i> Using a custom <code>TimeSource</code>.
 * </p>
 * <pre>
 * Stopwatch t = new Stopwatch( new JavaNanoTime() );
 * </pre>
 * 
 * @author tw team
 *
 */
public class Stopwatch {
	
	long totalTime;
	long currentStart;
	
	TimeSource timeImpl;
	
	/**
	 *  Constructs a fresh Stopwatch.<br />
	 *  TODO Should I mention here which TimeSource it defaults to?
	 */
	public Stopwatch() {
		timeImpl = new JavaSystemTime();
		init();
	}
	/**
	 * Constructs a fresh Stopwatch which will use the provided TimeSource.
	 * @param timeSource
	 */
	public Stopwatch( TimeSource timeSource ) {
		timeImpl = timeSource;
	}
	
	/**
	 * The common part of the various constructors.
	 */
	private void init() {
		totalTime = 0;
		currentStart = 0;
	}
	
	/**
	 * Start counting time.<br />
	 * Does nothing if the stopwatch is already started. This means that you
	 * cannot nest start()/stop() calls: a stop() always stops the counting
	 * of time, no matter how many start()s have gone in between.
	 */
	public void start() {
		if( currentStart==0 ) {
			currentStart = timeImpl.now();
		}
	}
	/**
	 * Stop counting time.<br />
	 * Does nothing if the stopwatch is not running. <emph>Always</emph> stops
	 * counting time: this means that you cannot nest start()/stop() calls.
	 */
	public void stop() {
		totalTime = getTime();
		currentStart = 0;
	}
	
	public void reset() {
		stop();
		totalTime = 0;
	}
	
	/**
	 * @return The current time on the stopwatch. What this number means depends
	 * on the TimeSource.
	 */
	public long getTime() {
		if( currentStart==0 ) {
			// currently not running
			return totalTime;
		} else {
			// currently running
			return totalTime + (timeImpl.now()-currentStart);
		}
	}
	
		

}
