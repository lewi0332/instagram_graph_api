post_insert = ("""INSERT INTO {table} (post_id,
                                        published_at,
                                        user_id,
                                        exits,
                                        replies,
                                        reach,
                                        taps_back,
                                        taps_forward,
                                        impressions)
                        VALUES (
                            %(id)s,
                            %(published_at)s::date,
                            %(media_id)s,
                            %(exits)s,
                            %(replies)s,
                            %(reach)s,
                            %(taps_back)s,
                            %(taps_forward)s,
                            %(impressions)s)
                        ON CONFLICT (post_id)
                        DO UPDATE SET (published_at,
                                        user_id,
                                        exits,
                                        replies,
                                        reach,
                                        taps_back,
                                        taps_forward,
                                        impressions) =
                            (
                            %(published_at)s,
                            %(media_id)s,
                            %(exits)s,
                            %(replies)s,
                            %(reach)s,
                            %(taps_back)s,
                            %(taps_forward)s,
                            %(impressions)s) \
                        WHERE {table}.post_id = %(id)s;""")
