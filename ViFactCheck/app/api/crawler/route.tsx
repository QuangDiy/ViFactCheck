import { NextResponse, NextRequest } from 'next/server';
import axios from 'axios';


async function crawlHtml(url: string): Promise<string> {
  try {
    const response = await axios.get(url);
    return response.data;
  } catch (error) {
    console.error('Error fetching HTML:', error);
    throw new Error('Failed to fetch HTML');
  }
}

export async function GET(request: NextRequest, { params }: any) {
  console.log(params);
  const url = request.nextUrl.searchParams.get('url')

  try {
    const html = await crawlHtml(url);
    return NextResponse.json(html);
  } catch (error) {
    return NextResponse.error();
  }
}